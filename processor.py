import pandas as pd

TECHNOLOGIES = ["Unix", "Windows", "SAP", "zOS"]

def process_incidents(current_file, previous_file, output_file):
    current_df = pd.read_excel(current_file)
    previous_df = pd.read_excel(previous_file)

    # Normalize text
    for col in ["Technology", "Application", "Root_Cause"]:
        current_df[col] = current_df[col].str.strip().str.lower()
        previous_df[col] = previous_df[col].str.strip().str.lower()

    writer = pd.ExcelWriter(output_file, engine="openpyxl")

    consolidated = []

    for tech in TECHNOLOGIES:
        curr_tech = current_df[current_df["Technology"] == tech.lower()]
        prev_tech = previous_df[previous_df["Technology"] == tech.lower()]

        recurrent = curr_tech.merge(
            prev_tech,
            on=["Application", "Root_Cause"],
            how="inner",
            suffixes=("_current", "_previous")
        )

        recurrent.to_excel(writer, sheet_name=f"{tech}_Recurrent", index=False)

        recurrent["Technology"] = tech
        consolidated.append(recurrent)

    # Consolidated Sheet
    if consolidated:
        final_df = pd.concat(consolidated)
        final_df.to_excel(writer, sheet_name="Consolidated_Recurrent", index=False)

    writer.close()
