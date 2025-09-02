# DICOM Anonymizer Pro 🛡️

A robust and easy-to-use Python script for anonymizing DICOM medical images. This tool removes Protected Health Information (PHI) from DICOM tags, creates a comprehensive backup of the original metadata, and ensures the resulting files are structurally sound for research and educational purposes.

## ✨ Key Features

  * **Comprehensive Metadata Backup**: Before any changes are made, all original metadata from each DICOM file is safely backed up into a single, easy-to-read text file.
  * **Targeted PHI Removal**: Scrubs sensitive patient information by removing specific DICOM tags, including Patient ID, Name, Birth Date, and more.
  * **UID Management**: Generates new `SOPInstanceUID`s for each file to prevent conflicts while preserving `StudyInstanceUID` and `SeriesInstanceUID` to maintain series integrity.
  * **Private Tag Removal**: Automatically removes all private tags, which can often contain sensitive institutional or vendor-specific information.
  * **Cross-Platform Compatibility**: Uses `pathlib` to automatically detect the user's Desktop, ensuring the script works seamlessly on Windows, macOS, and Linux.
  * **Data Integrity Checks**: Ensures essential tags like `Modality` and `ImageType` have default values if they are missing, preventing corrupted files.
  * **Consistent Series Numbering**: Sorts files alphabetically and re-assigns `InstanceNumber` sequentially to maintain a logical order within each series.

-----

## 🚀 How to Use

Getting started is simple. Just follow these steps:

#### 1\. Prerequisites

Ensure you have Python 3 installed on your system. You'll also need the `pydicom` library.

#### 2\. Installation

Install `pydicom` using pip:

```bash
pip install pydicom
```

#### 3\. Setup Your Folders

The script is designed to be user-friendly with a simple folder structure on your Desktop:

1.  Create a folder named **`originalDicom`** on your Desktop.
2.  Place all the DICOM files you want to anonymize inside this folder.

#### 4\. Run the Script

Execute the Python script from your terminal:

```bash
python test.py
```

The script will automatically create two new items on your Desktop:

  * 📁 A folder named **`anonymizedDicom`** containing the processed, safe-to-share files.
  * 📄 A log file named **`dicom_metadata_backup.txt`** containing the original metadata for all processed files.

-----

## ⚙️ Anonymization Details

This script takes a "remove and replace" approach to ensure confidentiality.

#### Tags Set to a New Value

| Tag Name | (Group, Element) | Action |
| :--- | :--- | :--- |
| `PatientName` | `(0x0010, 0x0010)` | Set to a static value: **"Patient 001"**. |
| `SOPInstanceUID` | `(0x0008, 0x0018)` | A new, unique UID is generated for each file. |
| `InstanceNumber` | `(0x0020, 0x0013)` | Re-numbered sequentially based on filename sort order. |

#### Sensitive Tags That Are Deleted

The following tags containing identifying information are **completely removed** from the files:

| Tag Name | (Group, Element) |
| :--- | :--- |
| Patient ID | `(0x0010, 0x0020)` |
| Patient Birth Date | `(0x0010, 0x0030)` |
| Patient Sex | `(0x0010, 0x0040)` |
| Other Patient IDs | `(0x0010, 0x1000)` |
| Referring Physician's Name | `(0x0008, 0x0090)` |
| Institution Name | `(0x0008, 0x0080)` |
| Station Name | `(0x0008, 0x1010)` |
| Institutional Department Name | `(0x0008, 0x1040)` |
| Operator's Name | `(0x0008, 0x1070)` |
| Accession Number | `(0x0008, 0x0050)` |
| Device Serial Number | `(0x0018, 0x1000)` |

#### Other Actions

  * **Private Tags**: All private tags (those with an odd Group number) are removed using `ds.remove_private_tags()`.
  * **Date/Time Tags**: All date and time tags are removed, except for `StudyDate`, `StudyTime`, `SeriesDate`, and `SeriesTime`, which are often necessary for chronological sorting.

-----

## ⚠️ Disclaimer

This script provides a strong baseline for DICOM anonymization. However, standards for de-identification can vary based on institutional review board (IRB) requirements, regional laws (like HIPAA or GDPR), and the nature of the data itself (e.g., "burned-in" annotations in pixel data).

**Always verify the output** of this script to ensure it meets the specific compliance and privacy requirements for your project. The authors are not liable for any data breaches that may result from improper use of this tool.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
