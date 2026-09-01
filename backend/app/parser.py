import re
from datetime import datetime


def parse_uipath_log(log_text):
    """
    Parses a UiPath execution log and returns a normalized incident.

    Args:
        log_text (str): Raw UiPath execution/job log.

    Returns:
        dict: Normalized incident information.
    """

    if not isinstance(log_text, str) or not log_text.strip():
        raise ValueError("Log text must be a non-empty string.")

    # ---------------------------------------------------------
    # Job Status
    # ---------------------------------------------------------

    status_match = re.search(
        r"\bState\s*\n\s*(Faulted|Successful|Stopped)\b",
        log_text,
        re.IGNORECASE
    )

    status = status_match.group(1).upper() if status_match else None

    # ---------------------------------------------------------
    # Process
    # ---------------------------------------------------------

    process_match = re.search(
        r"\bProcess\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    process = process_match.group(1).strip() if process_match else None

    # ---------------------------------------------------------
    # Package
    # ---------------------------------------------------------

    package_match = re.search(
        r"\bPackage\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    package = package_match.group(1).strip() if package_match else None

    # ---------------------------------------------------------
    # Package Version
    # ---------------------------------------------------------

    version_match = re.search(
        r"\bPackage\s+version\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    package_version = (
        version_match.group(1).strip()
        if version_match
        else None
    )

    # ---------------------------------------------------------
    # Exception Message
    # ---------------------------------------------------------

    raw_message_match = re.search(
        r"\bRaw message\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    exception_message = (
        raw_message_match.group(1).strip()
        if raw_message_match
        else None
    )

    # ---------------------------------------------------------
    # Exception Type
    # ---------------------------------------------------------

    exception_type_match = re.search(
        r"\b(?:System\.)?[\w.]+Exception\b",
        log_text
    )

    exception_type = (
        exception_type_match.group(0)
        if exception_type_match
        else None
    )

    # ---------------------------------------------------------
    # Workflow
    # ---------------------------------------------------------

    workflow_match = re.search(
        r"\bWorkflow\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    workflow = (
        workflow_match.group(1).strip()
        if workflow_match
        else None
    )

    # ---------------------------------------------------------
    # Activity
    # ---------------------------------------------------------

    activity_match = re.search(
        r"\bActivity\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    activity = (
        activity_match.group(1).strip()
        if activity_match
        else None
    )

    # ---------------------------------------------------------
    # Start Time
    # ---------------------------------------------------------

    start_match = re.search(
        r"\bStart Time\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    start_time = (
        _parse_datetime(start_match.group(1).strip())
        if start_match
        else None
    )

    # ---------------------------------------------------------
    # End Time
    # ---------------------------------------------------------

    end_match = re.search(
        r"\bEnd Time\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    end_time = (
        _parse_datetime(end_match.group(1).strip())
        if end_match
        else None
    )

    # ---------------------------------------------------------
    # Robot
    # ---------------------------------------------------------

    robot_match = re.search(
        r"\bRobot\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    robot = (
        robot_match.group(1).strip()
        if robot_match
        else None
    )

    # ---------------------------------------------------------
    # Machine / Hostname
    # ---------------------------------------------------------

    machine_match = re.search(
        r"\bHostname\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    machine = (
        machine_match.group(1).strip()
        if machine_match
        else None
    )

    # ---------------------------------------------------------
    # Account
    # ---------------------------------------------------------

    account_match = re.search(
        r"\bAccount\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    account = (
        account_match.group(1).strip()
        if account_match
        else None
    )

    # ---------------------------------------------------------
    # Execution Context
    # ---------------------------------------------------------

    input_match = re.search(
        r"\bInput Values\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    output_match = re.search(
        r"\bOutput Values\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    recording_match = re.search(
        r"\bHas Recording\s*:\s*(.+)",
        log_text,
        re.IGNORECASE
    )

    execution_context = {
        "input_values": (
            input_match.group(1).strip()
            if input_match
            else None
        ),
        "output_values": (
            output_match.group(1).strip()
            if output_match
            else None
        ),
        "has_recording": (
            recording_match.group(1).strip()
            if recording_match
            else None
        ),
        "account": account
    }

    # ---------------------------------------------------------
    # Normalized Incident
    # ---------------------------------------------------------

    incident = {
        "platform": "UiPath",
        "status": status,

        "process": process,
        "package": package,
        "package_version": package_version,

        "exception": {
            "message": exception_message,
            "type": exception_type
        },

        "workflow": workflow,
        "activity": activity,

        "timestamp": {
            "start": start_time,
            "end": end_time
        },

        "robot": robot,
        "machine": machine,

        "execution_context": execution_context
    }

    return incident


def _parse_datetime(value):
    """
    Converts common UiPath datetime strings into ISO format.
    """

    formats = [
        "%m/%d/%Y, %I:%M:%S %p",
        "%m/%d/%Y %I:%M:%S %p",
        "%Y-%m-%d %H:%M:%S"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).isoformat()
        except ValueError:
            continue

    # Return original value if format is unknown
    return value


# -------------------------------------------------------------
# Test / Demo
# -------------------------------------------------------------

if __name__ == "__main__":
    sample_log = """
    Job information

    Process: Payment_Process
    Package: PaymentAutomation
    Package version: 3.2.1

    State
    Faulted

    Raw message:

    Timeout reached.

    System.Runtime.InteropServices.COMException: Timeout reached.
    at UiPath.UIAutomationNext.Services.DriverService.Activate(UiNode uiNode)
    at UiPath.UIAutomationNext.Services.ActivityActionService.TypeInternal(...)
    at System.Threading.Tasks.Task.Execute()

    Workflow: Payment.xaml
    Activity: Type Into Card Number

    Start Time: 7/20/2026, 6:30:15 PM
    End Time: 7/20/2026, 6:31:02 PM

    Robot: payment-bot
    Hostname: UAT-BOT-01
    Account: automation-account

    Input Values: CardNumber=*****
    Output Values: Empty
    Has Recording: false
    """

    incident = parse_uipath_log(sample_log)

    print("Parsed Incident:\n")
    print(incident)