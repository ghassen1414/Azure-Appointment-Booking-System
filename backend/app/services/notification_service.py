
from azure.communication.email import EmailClient
from app.core.config import settings
import logging
import datetime 
from typing import Optional, List 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _send_email_acs(
    recipient_email: str,
    recipient_name: str,
    subject: str,
    plain_text_content: str,
    html_content: str
) -> bool:
    """Helper function to send email via ACS."""
    if not settings.ACS_CONNECTION_STRING or not settings.ACS_SENDER_ADDRESS:
        logger.error("ACS_CONNECTION_STRING or ACS_SENDER_ADDRESS is not configured. Email not sent.")
        return False
    try:
        email_client = EmailClient.from_connection_string(settings.ACS_CONNECTION_STRING)
        message = {
            "content": {"subject": subject, "plainText": plain_text_content, "html": html_content},
            "recipients": {"to": [{"address": recipient_email, "displayName": recipient_name}]},
            "senderAddress": settings.ACS_SENDER_ADDRESS
        }
        poller = email_client.begin_send(message)
        logger.info(f"Email send operation to {recipient_email} for subject '{subject}' started with ID: {poller.id()}. Status: {poller.status()}")
        # For simplicity, returning True if initiated. Add poller.result() for robust status check.
        return True
    except Exception as e:
        logger.error(f"An error occurred while sending email to {recipient_email} for subject '{subject}': {e}")
        return False

def format_datetime_for_email(dt_object: Optional[datetime.datetime]) -> str:
    """Helper to format datetime objects for email, handling None."""
    if dt_object is None:
        return "N/A"
    return dt_object.strftime('%Y-%m-%d at %H:%M') # Example format

def send_appointment_created_email(
    recipient_email: str,
    recipient_name: str,
    appointment_details: dict # Expects keys: service_name, start_time, end_time, status, notes, id
) -> bool:
    subject = f"Appointment Confirmed: {appointment_details.get('service_name', 'Your Appointment')}"
    
    start_time_str = format_datetime_for_email(appointment_details.get('start_time'))
    end_time_str = format_datetime_for_email(appointment_details.get('end_time'))
    status_str = str(appointment_details.get('status').value) if appointment_details.get('status') else 'N/A'
    appointment_id = appointment_details.get('id', 'N/A')

    plain_text_content = f"""
    Hello {recipient_name if recipient_name else 'User'},

    Your appointment has been successfully booked!

    *** Your Appointment ID is: {appointment_id} ***
    Please use this ID to manage your appointment.

    Details:
    Service: {appointment_details.get('service_name', 'N/A')}
    Time: {start_time_str} to {end_time_str}
    Status: {status_str}
    Notes: {appointment_details.get('notes', 'None')}

    Thank you!
    """
    html_content = f"""
    <html><body>
        <p>Hello {recipient_name if recipient_name else 'User'},</p>
        <p>Your appointment has been successfully booked!</p>
        <p><strong>Your Appointment ID is: {appointment_id}</strong><br>
        <small>Please use this ID to manage your appointment on our website.</small></p>
        <h3>Details:</h3><ul>
            <li><strong>Service:</strong> {appointment_details.get('service_name', 'N/A')}</li>
            <li><strong>Time:</strong> {start_time_str} to {end_time_str}</li>
            <li><strong>Status:</strong> {status_str}</li>
            <li><strong>Notes:</strong> {appointment_details.get('notes', 'None')}</li>
        </ul><p>Thank you!</p>
    </body></html>
    """
    return _send_email_acs(recipient_email, recipient_name, subject, plain_text_content, html_content)

def send_appointment_updated_email(
    recipient_email: str,
    recipient_name: str,
    appointment_details: dict, # Expects current appointment details
    old_appointment_details: Optional[dict] = None # Optional: For showing what changed
) -> bool:
    subject = f"Appointment Updated: {appointment_details.get('service_name', 'Your Appointment')}"

    appointment_id = appointment_details.get('id', 'N/A') # Get the ID
    current_start_str = format_datetime_for_email(appointment_details.get('start_time'))
    current_end_str = format_datetime_for_email(appointment_details.get('end_time'))
    current_status_str = str(appointment_details.get('status').value) if appointment_details.get('status') else 'N/A'
    current_notes_str = appointment_details.get('notes', 'None')
    current_service_name = appointment_details.get('service_name', 'N/A')

    changes_summary = ""
    if old_appointment_details:
        old_start_str = format_datetime_for_email(old_appointment_details.get('start_time'))
        old_end_str = format_datetime_for_email(old_appointment_details.get('end_time'))
        old_status_str = str(old_appointment_details.get('status').value) if old_appointment_details.get('status') else 'N/A'

        if old_start_str != current_start_str or old_end_str != current_end_str:
            changes_summary += f"    - Time changed from: {old_start_str} - {old_end_str}\\n"
        if old_status_str != current_status_str:
            changes_summary += f"    - Status changed from: {old_status_str}\\n"
        # Add more change detections if needed (e.g., notes, service_name)

    plain_text_content = f"""
    Hello {recipient_name if recipient_name else 'User'},

    <p>Your appointment (ID: {appointment_id}) has been updated.</p>

    New Details:
    Service: {current_service_name}
    Time: {current_start_str} to {current_end_str}
    Status: {current_status_str}
    Notes: {current_notes_str}
    """
    if changes_summary:
        plain_text_content += f"\nSummary of Changes:\n{changes_summary}"
    plain_text_content += "\nThank you!"

    html_content = f"""
    <html><body>
        <p>Hello {recipient_name if recipient_name else 'User'},</p>
        <p>Your appointment has been updated.</p>
        <h3>New Details:</h3><ul>
            <li><strong>Service:</strong> {current_service_name}</li>
            <li><strong>Time:</strong> {current_start_str} to {current_end_str}</li>
            <li><strong>Status:</strong> {current_status_str}</li>
            <li><strong>Notes:</strong> {current_notes_str}</li>
        </ul>
    """
    if changes_summary:
        html_content += f"<h3>Summary of Changes:</h3><pre>{changes_summary.replacechr(10, '<br>')}</pre>" # Crude pre for now
    html_content += "<p>Thank you!</p></body></html>"

    return _send_email_acs(recipient_email, recipient_name, subject, plain_text_content, html_content)

def send_appointment_cancelled_email(
    recipient_email: str,
    recipient_name: str,
    appointment_details: dict # Details of the appointment that was cancelled
) -> bool:
    subject = f"Appointment Cancelled: {appointment_details.get('service_name', 'Your Appointment')}"
    
    start_time_str = format_datetime_for_email(appointment_details.get('start_time'))
    end_time_str = format_datetime_for_email(appointment_details.get('end_time'))
    service_name = appointment_details.get('service_name', 'N/A')

    plain_text_content = f"""
    Hello {recipient_name if recipient_name else 'User'},

    Your appointment has been cancelled.

    Cancelled Appointment Details:
    Service: {service_name}
    Originally Scheduled For: {start_time_str} to {end_time_str}

    If this was a mistake or you wish to rebook, please contact us or visit our booking page.
    Thank you.
    """
    html_content = f"""
    <html><body>
        <p>Hello {recipient_name if recipient_name else 'User'},</p>
        <p>Your appointment has been cancelled.</p>
        <h3>Cancelled Appointment Details:</h3><ul>
            <li><strong>Service:</strong> {service_name}</li>
            <li><strong>Originally Scheduled For:</strong> {start_time_str} to {end_time_str}</li>
        </ul>
        <p>If this was a mistake or you wish to rebook, please contact us or visit our booking page.</p>
        <p>Thank you.</p>
    </body></html>
    """
    return _send_email_acs(recipient_email, recipient_name, subject, plain_text_content, html_content)

# Original function (can be kept for direct use or refactored if it was generic enough)
# For now, we'll assume the specific functions above are preferred.
# def send_appointment_confirmation_email(...) -> This was the previous generic one.