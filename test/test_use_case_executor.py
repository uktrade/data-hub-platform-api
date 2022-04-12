import pytest

from platform_api.use_case_executor import UseCaseExecutor, UseCaseNotFoundError, UseCaseMissingCallDunderMethodError


def test_can_provide_useful_error_when_use_case_not_found():
    with pytest.raises(UseCaseNotFoundError):
        UseCaseExecutor()('not-found')


class IncorrectlyDefinedUseCase:
    pass


def test_can_provide_useful_error_when_use_case_not_properly_defined():
    with pytest.raises(UseCaseMissingCallDunderMethodError):
        executor = UseCaseExecutor()
        executor.use_cases['incorrectly-defined'] = IncorrectlyDefinedUseCase()
        executor('incorrectly-defined')
