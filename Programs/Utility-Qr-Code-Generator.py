# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools
# See the file 'LICENSE' for copying permission.
# --------------------------------------------------------
# EN: Non-commercial use only. Do not sell, remove credits
#     or redistribute without prior written permission.
# FR: Usage non-commercial uniquement. Ne pas vendre, supprimer
#     les crédits ou redistribuer sans autorisation écrite.

from Core.Utils import *
from Core.Config import *

try:
    import qrcode
    import os
    import re
except Exception as e:
    MissingModule(e)

Title("Qr Code Generator")

Scroll(GradientBanner(utilities_banner))

try:
    data = input(f"{INPUT} Data {red}->{reset} ").strip()

    if not data:
        ErrorInput()

    name = input(f"{INPUT} File Name {red}->{reset} ").strip()

    if not name:
        ErrorInput()

    name = re.sub(r'[\\/*?:"<>|]', "", name).strip()

    if not name:
        print(f"{ERROR} Invalid file name!", reset)
        Continue()
        Reset()

    print(f"{LOADING} Generating..", reset)

    try:
        output_dir = os.path.join(tool_path, "Programs", "Output", "QrCodeGenerator")
        os.makedirs(output_dir, exist_ok=True)

        qr = qrcode.QRCode(
            version         = 1,
            error_correction= qrcode.constants.ERROR_CORRECT_H,
            box_size        = 10,
            border          = 4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img  = qr.make_image(fill_color="black", back_color="white")
        path = os.path.join(output_dir, f"{name}.png")
        img.save(path)

        print(f"{SUCCESS} Saved:{red} {path}", reset)

        if platform_pc == "Windows":
            os.startfile(output_dir)
        else:
            subprocess.Popen(["xdg-open", output_dir])

    except Exception:
        print(f"{ERROR} Could not generate Qr Code!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)