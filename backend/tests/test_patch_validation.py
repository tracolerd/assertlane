import os
import sys

import pytest
from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import schemas


@pytest.mark.parametrize(
    "model,field",
    [
        (schemas.ProjectUpdate, "name"),
        (schemas.TestSuiteUpdate, "name"),
        (schemas.TestCaseUpdate, "title"),
        (schemas.TestCaseUpdate, "steps"),
        (schemas.TestCaseUpdate, "expected_result"),
        (schemas.TestRunUpdate, "name"),
        (schemas.TestRunUpdate, "status"),
    ],
)
def test_patch_rejects_explicit_null_for_non_nullable_fields(model, field):
    with pytest.raises(ValidationError):
        model(**{field: None})


@pytest.mark.parametrize(
    "model",
    [
        schemas.ProjectUpdate,
        schemas.TestSuiteUpdate,
        schemas.TestCaseUpdate,
        schemas.TestRunUpdate,
    ],
)
def test_patch_omitted_fields_remain_unchanged(model):
    payload = model()
    assert payload.model_dump(exclude_unset=True) == {}


def test_patch_allows_explicit_null_for_nullable_fields():
    project = schemas.ProjectUpdate(description=None)
    case = schemas.TestCaseUpdate(preconditions=None, tags=None)
    assert project.model_dump(exclude_unset=True) == {"description": None}
    assert case.model_dump(exclude_unset=True) == {"preconditions": None, "tags": None}
