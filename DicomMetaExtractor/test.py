# Set input/output directories
'''input_folder = "/Users/anonymous/Desktop/originalDicom"
output_folder = "/Users/anonymous/Desktop/anonymizedDicom"
metadata_log = "/Users/anonymous/Desktop/metadata_backup.txt" '''

import os
import pydicom
from pydicom.uid import generate_uid
from pathlib import Path
# Get cross-platform Desktop path
desktop = Path.home() / "Desktop"

# Cross-platform folders and log file
input_folder = desktop / "originalDicom"
output_folder = desktop / "anonymizedDicom"
metadata_log = desktop / "dicom_metadata_backup.txt"

'''
# --- Input/output paths (update for your system) ---
input_folder = "/Users/anonymous/Desktop/originalDicom"
output_folder = "/Users/anonymous/Desktop/anonymizedDicom"
metadata_log = "/Users/anonymous/Desktop/metadata_backup.txt"
'''


os.makedirs(output_folder, exist_ok=True)

# Helper function to sanitize metadata for logging
def safe_str(value):
    try:
        if isinstance(value, bytes):
            if len(value) > 128:
                return "<binary data omitted>"
            return value.decode(errors='replace')
        return str(value)
    except:
        return "<unreadable>"

# Sort files for consistent InstanceNumber assignment
dicom_files = sorted(os.listdir(input_folder))

# --- Backup log ---
with open(metadata_log, "w", encoding="utf-8") as meta_file:

    for idx, filename in enumerate(dicom_files):
        input_path = os.path.join(input_folder, filename)

        try:
            ds = pydicom.dcmread(input_path, force=True)

            # --- BACKUP METADATA ---
            meta_file.write(f"----- {filename} -----\n")
            for elem in ds:
                try:
                    tag = elem.tag
                    name = elem.name
                    value = safe_str(elem.value)
                    meta_file.write(f"{tag} {name}: {value}\n")
                except:
                    meta_file.write(f"{elem.tag} <error reading>\n")
            meta_file.write("\n\n")

            # --- ANONYMIZE: Set same PatientName for all ---
            ds.PatientName = "Patient 001"

            # --- REMOVE SENSITIVE TAGS ---
            sensitive_tags = [
                (0x0010, 0x0020),  # Patient ID
                (0x0010, 0x0030),  # Birth Date
                (0x0010, 0x0040),  # Sex
                (0x0008, 0x0090),  # Referring Physician
                (0x0008, 0x0080),  # Institution Name
                (0x0008, 0x1010),  # Station Name
                (0x0008, 0x1040),  # Department Name
                (0x0008, 0x1070),  # Operator's Name
                (0x0018, 0x1000),  # Device Serial Number
                (0x0008, 0x0050),  # Accession Number
                (0x0010, 0x1000),  # Other Patient IDs
            ]

            for tag in sensitive_tags:
                if tag in ds:
                    del ds[tag]

            # --- PRESERVE ORIGINAL GROUPING TAGS ---
            if not hasattr(ds, 'StudyInstanceUID'):
                ds.StudyInstanceUID = generate_uid()
            if not hasattr(ds, 'SeriesInstanceUID'):
                ds.SeriesInstanceUID = generate_uid()
            if not hasattr(ds, 'FrameOfReferenceUID'):
                ds.FrameOfReferenceUID = generate_uid()

            # Force new SOPInstanceUID
            ds.SOPInstanceUID = generate_uid()

            # --- KEEP ORIGINAL SeriesDescription etc. ---
            if not hasattr(ds, "SeriesDescription"):
                ds.SeriesDescription = "Unknown Series"

            ds.Modality = ds.get("Modality", "OT")
            ds.BodyPartExamined = ds.get("BodyPartExamined", "UNKNOWN")
            ds.ImageType = ds.get("ImageType", ["ORIGINAL", "PRIMARY", "AXIAL"])
            ds.InstanceNumber = idx + 1

            # Fix orientation (safe default)
            ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]

            # --- Remove private + non-essential date/time tags ---
            ds.remove_private_tags()
            safe_time_tags = ["StudyDate", "StudyTime", "SeriesDate", "SeriesTime"]
            for tag in ds.dir():
                if ("Date" in tag or "Time" in tag) and tag not in safe_time_tags:
                    try:
                        delattr(ds, tag)
                    except:
                        pass

            # --- Save anonymized DICOM ---
            output_path = os.path.join(output_folder, filename)
            ds.save_as(output_path)

            print(f"[✔] Anonymized: {filename}")

        except Exception as e:
            print(f"[!] Skipping {filename}: {e}")
