import ingest


if __name__ == "__main__":
    df_inpatient = ingest.get_inpatient()
    print(f"Shape: {df_inpatient.shape}")
    print(f"Columns: {df_inpatient.columns}")
    print(f"Describe: {df_inpatient.describe()}")

    df_outpatient = ingest.get_outpatient()
    print(f"Shape: {df_outpatient.shape}")
    print(f"Columns: {df_outpatient.columns}")
    print(f"Describe: {df_outpatient.describe()}")
