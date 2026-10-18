const fs = require('fs');
const path = require('path');
async function pushResults() {
  const runId = process.env.ASSERTLANE_RUN_ID;
  if (!runId) throw new Error("ASSERTLANE_RUN_ID is missing.");
  const reportPath = path.join(__dirname, 'results.json');
  const data = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
  function extractResults(suites, resultsArr = []) {
    for (const suite of suites) {
      for (const spec of suite.specs || []) {
        const match = spec.title.match(/@TID-([a-zA-Z0-9-]+)/);
        if (match && spec.tests && spec.tests[0].results) {
          const result = spec.tests[0].results[0];
          let status = "Skipped";
          if (result.status === 'passed') status = "Passed";
          if (result.status === 'failed') status = "Failed";
          if (result.status === 'timedOut') status = "Error";
          resultsArr.push({
            test_case_id: match[1],
            status: status,
            execution_time_ms: result.duration || 0
          });
        }
      }
      if (suite.suites) extractResults(suite.suites, resultsArr);
    }
    return resultsArr;
  }
  const formattedResults = extractResults(data.suites || []);
  if (formattedResults.length === 0) {
    console.log("No tagged tests found to upload.");
    return;
  }
  console.log(`Sending ${formattedResults.length} results to AssertLane...`);
  const response = await fetch(`http://127.0.0.1:8000/api/runs/${runId}/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reporter: "playwright-local", results: formattedResults })
  });
  const responseData = await response.json();
  console.log("AssertLane Import Response:", responseData);
}
pushResults().catch(console.error);
