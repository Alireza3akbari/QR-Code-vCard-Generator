import os
import qrcode

def make_vcard(first_name: str, last_name: str, phone: str, org: str = "", email: str = "") -> str:
    """
    Create a vCard string for contact information.
    """
    # Clean phone number (allow only digits and '+')
    phone = "".join(ch for ch in phone if ch.isdigit() or ch == '+')

    # Build the vCard 3.0 format
    vcard_lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{last_name};{first_name};;;",
        f"FN:{first_name} {last_name}",
    ]
    if org:
        vcard_lines.append(f"ORG:{org}")
    if email:
        vcard_lines.append(f"EMAIL;TYPE=INTERNET:{email}")
    if phone:
        vcard_lines.append(f"TEL;TYPE=CELL:{phone}")

    vcard_lines.append("END:VCARD")
    return "\n".join(vcard_lines)


def save_qr(data: str, out_path: str, box_size: int = 10, border: int = 4):
    """
    Generate and save QR code as PNG file.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_path)
    print(f"QR saved -> {out_path}")


if __name__ == "__main__":
    # Get user input
    first = input("First name: ").strip()
    last = input("Last name (optional): ").strip()
    phone = input("Phone number (+98... or 0912...): ").strip()
    org = input("Organization / Company (optional): ").strip()
    email = input("Email (optional): ").strip()

    # Create vCard
    vcard_text = make_vcard(first_name=first, last_name=last, phone=phone, org=org, email=email)

    # Output folder
    out_dir = "qrcodes"
    os.makedirs(out_dir, exist_ok=True)

    # Safe file name
    safe_name = (first + "_" + last).strip().replace(" ", "_") or "contact"
    filename = f"{safe_name}_{phone}.png"
    out_path = os.path.join(out_dir, filename)

    # Generate QR code image
    save_qr(vcard_text, out_path)

    # Debug output
    print("\n--- vCard content ---")
    print(vcard_text)
    print("----------------------")
    print("The QR code is ready! When scanned, it will show the contact details and allow saving to the phone.")
