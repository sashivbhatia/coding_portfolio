# Pytest UAT Reporting Framework  

## Overview  
This project contains a **custom Pytest configuration (`conftest.py`)** developed during my internship at Bunge.  
It was designed to support the **Market Risk team’s user acceptance testing (UAT)** by enabling flexible test selection, automating result compilation, and producing clear, shareable reports.  

⚠️ Note: The actual tests written for production are proprietary and cannot be shared.  
This repository instead showcases the **reporting and orchestration layer** I built.  

## Features  
- **Custom Test Selection:**  
  - Run specific tests using a `--tests` command-line option or a `test_selection.txt` file.  

- **HTML Reporting:**  
  - Automatically generates daily HTML reports with dynamic titles.  
  - Displays passed/failed test cases with formatting (failed cases in red, truncation of long lists).  
  - Adds descriptive columns and custom metadata for each test.  

- **Excel Integration:**  
  - Creates a companion Excel workbook (`.xlsx`) with detailed test case results.  
  - Provides a downloadable Excel link inside the HTML report.  

- **Custom Fixtures & Hooks:**  
  - Tracks failed cases and their details (database values, additional info, etc.).  
  - Extends Pytest hooks (`pytest_html_*`, `pytest_configure`, `pytest_runtest_makereport`) to enrich output.  

## Tech Stack  
- **Python**  
- **Pytest** + `pytest-html`  
- **OpenPyXL** for Excel reporting  
- **Base64** encoding for embedding downloadable files into reports  

## Example Workflow  
1. Define tests with Pytest markers (not included here due to sensitivity).  
2. Specify tests in `test_selection.txt` or select tests to run using:
   
   ```bash
   pytest -m "marker_name" --html=report.html
  
3. View results:
- Open the HTML report for an interactive summary.  
- Download the Excel report directly from within the HTML.  

---

## Context
This framework was part of a larger effort to ensure data accuracy and consistency across multiple databases in financial risk management. It provided:
- Daily automated checks  
- A maintainable reporting system  
- A collaborative testing environment for the Market Risk team  
   pytest -m "marker_name" --html=report.html

