<p align="center">
  <img src="../assets/assertlane-banner.svg" alt="AssertLane animated banner" width="100%" />
</p>

<h1 align="center">AssertLane Frontend</h1>

<p align="center">
  <strong>React + TypeScript + Vite project UI.</strong>
</p>

<p align="center">
  <a href="../README.md">Root README</a> ·
  <a href="../docs/RELEASE_AUDIT.md">Release readiness audit</a> ·
  <a href="https://assertlane.netlify.app/">Frontend preview</a>
</p>

## Current scope

The current frontend provides a small project dashboard that displays backend status and lets a user create and list projects. Suite, case, test-run, and test-result workflows are currently represented by backend API routes, not complete frontend screens.

## Stack

- React 19 and TypeScript
- Vite
- Tailwind CSS
- Axios for HTTP requests

## Local setup

From this directory:

```bash
npm ci
npm run dev
```

The current source hard-codes the API origin as `http://127.0.0.1:8000`. Before using the UI from a different browser origin, make the API URL configurable and add a strict CORS allowlist to FastAPI. A hosted frontend does not make a local API available to remote visitors.

Create a static production bundle with:

```bash
npm run build
npm run preview
```

The production frontend is only a static site; the API must be deployed separately and configured before end-to-end hosted use can work.

## Security note

The current backend has no authentication or authorization controls. Do not use this frontend with confidential test evidence or against a publicly exposed API until the blockers in the [release audit](../docs/RELEASE_AUDIT.md) are resolved.
---

## Creator, Developer & Maintainer

**Created, designed, developed, and maintained by [Nurul Faiyaz](https://github.com/tracolerd).**

This project is independently built and maintained by Nurul Faiyaz. The project's design, implementation, and documentation are his work.

<p align="center">
  <a href="https://www.facebook.com/faiyaz.888"><img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook" /></a>
  <a href="https://www.instagram.com/tracolerd"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" /></a>
  <a href="https://www.linkedin.com/in/faiyaz-xyz"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://x.com/faiyaz_explores"><img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X" /></a>
  <a href="https://github.com/tracolerd"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="mailto:scrollfaiyaz@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="https://nurul-faiyaz.netlify.app/"><img src="https://img.shields.io/badge/Portfolio-Visit%20Website-0F766E?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Personal website" /></a>
</p>

<p align="center">
  <a href="https://www.facebook.com/faiyaz.888">Facebook</a> ·
  <a href="https://www.instagram.com/tracolerd">Instagram</a> ·
  <a href="https://www.linkedin.com/in/faiyaz-xyz">LinkedIn</a> ·
  <a href="https://x.com/faiyaz_explores">X / Twitter</a> ·
  <a href="https://github.com/tracolerd">GitHub</a> ·
  <a href="mailto:scrollfaiyaz@gmail.com">Email</a> ·
  <a href="https://nurul-faiyaz.netlify.app/">Website</a>
</p>
