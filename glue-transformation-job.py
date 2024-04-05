def ExtractRequirements (glueContext, dfc) -> DynamicFrameCollection:
    from pyspark.sql.functions import udf
    from pyspark.sql.types import ArrayType, StringType
    
    # Function to extract requirements from description
    def extract_requirements(description):
        import re
        # Join all description sections into a single string
        description_text = ' '.join(description)
       
        # Define possible titles for the requirements section
        titles = ['Requirements', 'Qualifications', 'Key Requirements', 'Skills Required', 'Basic Qualifications']
       
        # Construct the regex pattern
        pattern = r'({})[\s,:]*\s*(?:.*?\n)?\s*(.*?)\s*(?:$)'.format('|'.join(titles))
       
        # Use regex to extract requirements
        match = re.search(pattern, description_text, re.IGNORECASE | re.DOTALL)
       
        # If a match is found
        if match:
            # Extract the requirements text
            requirements = match.group(2).strip()
     
            # Truncate the requirements text if it exceeds 500 bytes
            if len(requirements.encode('utf-8')) > 500:
                requirements = requirements[:500].rsplit(' ', 1)[0] # Truncate at the last space before 1400 bytes
     
            return requirements
        else:
            return ""
       
    # Convert DynamicFrame to DataFrame
    input_df = dfc.select(list(dfc.keys())[0]).toDF()
    
    extract_requirements_udf = udf(extract_requirements, StringType())
    # Apply UDF to extract requirements and add as a new column
    output_df = input_df.withColumn("requirements", extract_requirements_udf(input_df["description"])).drop("description")
       
    # Convert DataFrame back to DynamicFrame
    output_dyf = DynamicFrame.fromDF(output_df, glueContext, "output_dyf")
       
    # Return DynamicFrameCollection
    return DynamicFrameCollection({"output_dyf": output_dyf}, glueContext)