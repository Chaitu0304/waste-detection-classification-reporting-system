import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime
import pandas as pd

try:
    from dotenv import load_dotenv
    # Search for .env in current directory, parent directory, and workspace root
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
    load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

try:
    import streamlit as st
except ImportError:
    st = None


def get_email_config():
    """
    Retrieves email configuration from environment variables or Streamlit secrets.
    Returns a dict with all necessary connection parameters and flags indicating missing fields.
    """
    config = {
        "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "465")),
        "smtp_username": os.getenv("SMTP_USERNAME") or os.getenv("SENDER_EMAIL") or "",
        "smtp_password": os.getenv("SMTP_PASSWORD") or "",
        "admin_email": os.getenv("ADMIN_EMAIL") or "",
        "sender_email": os.getenv("SENDER_EMAIL") or os.getenv("SMTP_USERNAME") or "",
        "source": "environment",
    }

    # Fallback to Streamlit secrets if running in Streamlit
    if st is not None:
        try:
            # Check for nested [email] section in secrets.toml
            email_secrets = st.secrets.get("email", {})
            if email_secrets:
                config["smtp_host"] = email_secrets.get("host", config["smtp_host"])
                config["smtp_port"] = int(email_secrets.get("port", config["smtp_port"]))
                config["smtp_username"] = email_secrets.get("sender", email_secrets.get("username", config["smtp_username"]))
                config["smtp_password"] = email_secrets.get("password", config["smtp_password"])
                config["admin_email"] = email_secrets.get("admin", email_secrets.get("admin_email", config["admin_email"]))
                config["sender_email"] = email_secrets.get("sender", config["sender_email"]) or config["smtp_username"]
                config["source"] = "st.secrets"
            else:
                # Check top-level keys in secrets.toml
                if "SMTP_USERNAME" in st.secrets:
                    config["smtp_username"] = st.secrets.get("SMTP_USERNAME", config["smtp_username"])
                    config["smtp_password"] = st.secrets.get("SMTP_PASSWORD", config["smtp_password"])
                    config["admin_email"] = st.secrets.get("ADMIN_EMAIL", config["admin_email"])
                    config["smtp_host"] = st.secrets.get("SMTP_HOST", config["smtp_host"])
                    config["smtp_port"] = int(st.secrets.get("SMTP_PORT", config["smtp_port"]))
                    config["sender_email"] = st.secrets.get("SENDER_EMAIL", config["smtp_username"])
                    config["source"] = "st.secrets"
        except Exception:
            # secrets.toml may not exist, which is fine
            pass

    return config


def validate_email_config(config=None):
    """
    Validates if the email configuration has all required fields.
    Returns (is_valid: bool, missing_fields: list, error_message: str)
    """
    if config is None:
        config = get_email_config()

    missing = []
    if not config.get("smtp_username"):
        missing.append("SMTP_USERNAME (or SENDER_EMAIL)")
    if not config.get("smtp_password"):
        missing.append("SMTP_PASSWORD")
    if not config.get("admin_email"):
        missing.append("ADMIN_EMAIL")

    if missing:
        msg = (
            f"Email service configuration missing: {', '.join(missing)}. "
            "Please configure these in your .env file or .streamlit/secrets.toml."
        )
        return False, missing, msg

    return True, [], ""


def send_waste_report_email(
    report_df: pd.DataFrame,
    report_csv: bytes,
    pdf_path: str = None,
    summary_metrics: dict = None,
    image_name: str = "detected_waste_sample.jpg"
):
    """
    Prepares and sends a structured waste detection report to the administrator email address.
    Attaches both the CSV audit log and the PDF report if available.
    
    Returns (success: bool, status_message: str)
    """
    config = get_email_config()
    is_valid, missing, err_msg = validate_email_config(config)

    if not is_valid:
        return False, err_msg

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_items = summary_metrics.get("total_items", len(report_df)) if summary_metrics else len(report_df)
        unique_categories = summary_metrics.get("unique_categories", len(report_df)) if summary_metrics else len(report_df)
        dominant_category = summary_metrics.get("dominant_category", "N/A") if summary_metrics else "N/A"

        # Build clean plain-text table
        table_str = report_df.to_string(index=False)

        # Create EmailMessage
        msg = EmailMessage()
        msg["Subject"] = f"[WasteAI Report] Detection Summary - {dominant_category} dominant ({total_items} items)"
        msg["From"] = config["sender_email"]
        msg["To"] = config["admin_email"]

        # Plaintext Body
        text_content = (
            f"WasteAI - Smart Waste Intelligence Detection Report\n"
            f"{'='*60}\n\n"
            f"Dear Waste Management Administrator,\n\n"
            f"A waste detection session has been processed by WasteAI YOLOv8 computer vision.\n\n"
            f"SESSION SUMMARY:\n"
            f"--------------------------------------------------\n"
            f"  Timestamp:               {timestamp}\n"
            f"  Analyzed Source:         {image_name}\n"
            f"  Total Waste Objects:     {total_items}\n"
            f"  Identified Categories:   {unique_categories}\n"
            f"  Dominant Waste Stream:   {dominant_category}\n\n"
            f"DETAILED BREAKDOWN BY MATERIAL CATEGORY:\n"
            f"--------------------------------------------------\n"
            f"{table_str}\n\n"
            f"{'='*60}\n"
            f"ATTACHMENTS:\n"
            f"  1. waste_detection_report.csv  (Structured tabular log)\n"
        )
        if pdf_path and Path(pdf_path).exists():
            text_content += f"  2. {Path(pdf_path).name}  (Visual executive PDF report)\n"

        text_content += (
            f"\n\nThis is an automated operational notification dispatched by WasteAI.\n"
            f"System: Waste Detection, Classification & Reporting Platform\n"
        )

        msg.set_content(text_content)

        # Attach CSV
        if report_csv:
            msg.add_attachment(
                report_csv,
                maintype="text",
                subtype="csv",
                filename="waste_detection_report.csv"
            )

        # Attach PDF if available
        if pdf_path and Path(pdf_path).exists():
            try:
                with open(pdf_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                    msg.add_attachment(
                        pdf_bytes,
                        maintype="application",
                        subtype="pdf",
                        filename=Path(pdf_path).name
                    )
            except Exception as pe:
                print(f"[Warning] Failed to read PDF for attachment: {pe}")

        # Connect and send via SMTP
        smtp_host = config["smtp_host"]
        smtp_port = config["smtp_port"]
        smtp_user = config["smtp_username"]
        smtp_pass = config["smtp_password"]

        if smtp_port == 465:
            # SSL Connection
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20) as server:
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        else:
            # TLS Connection (port 587 or other)
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

        return True, f"Report successfully dispatched to administrator ({config['admin_email']}) via {smtp_host}."

    except smtplib.SMTPAuthenticationError:
        return False, (
            "SMTP Authentication failed: Invalid username or password. "
            "For Gmail accounts, ensure you are using a 16-character Google App Password (not your primary password) "
            "with 2-Step Verification enabled."
        )
    except smtplib.SMTPConnectError as ce:
        return False, f"Could not connect to SMTP server ({config['smtp_host']}:{config['smtp_port']}): {ce}"
    except smtplib.SMTPRecipientsRefused:
        return False, f"The administrator recipient address ({config['admin_email']}) was rejected by the mail server."
    except Exception as ex:
        return False, f"Failed to deliver email: {str(ex)}"
