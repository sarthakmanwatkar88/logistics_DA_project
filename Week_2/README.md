Week 2 — Logistics Data Preprocessing and Data Quality Analysis
Internship Project

Week 2 of my Data Science and Analytics internship focuses on data collection simulation, data cleaning, preprocessing, outlier analysis, normalization, and validation using a logistics delivery dataset.

Objective

The main objective of this task is to prepare a high-quality logistics dataset for further analysis and machine learning applications.

The preprocessing process focuses on:

Data collection and initial inspection
Data quality assessment
Missing value analysis
Duplicate record analysis
Data type and format cleaning
Outlier detection
Data normalization
Final dataset validation
Dataset Information

The dataset used for this task is Delivery_Logistics.csv.

The dataset contains 25,000 records and 15 variables related to logistics and delivery operations.

Dataset Variables
Variable	Description
delivery_id	Identifier associated with a delivery
delivery_partner	Delivery partner handling the shipment
package_type	Type of package
vehicle_type	Vehicle used for delivery
delivery_mode	Mode of delivery
region	Delivery region
weather_condition	Weather condition during delivery
distance_km	Delivery distance in kilometres
package_weight_kg	Package weight in kilograms
delivery_time_hours	Actual delivery time
expected_time_hours	Expected delivery time
delayed	Indicates whether the delivery was delayed
delivery_status	Final delivery status
delivery_rating	Delivery rating
delivery_cost	Delivery cost
Data Quality Assessment

The dataset was initially inspected to identify possible data-quality issues.

The initial analysis showed:

Total records: 25,000
Total columns: 15
Complete duplicate rows: 0
Missing values: 0
Unique delivery IDs: 24,502
Repeated delivery IDs: 498

The presence of repeated delivery IDs was investigated separately from complete duplicate rows because repeated identifiers do not necessarily mean that the entire records are duplicates.

Missing Value Analysis

Missing values were checked across all columns.

The dataset contained no missing values.

Therefore, no rows needed to be removed and no missing-value imputation technique was required.

This confirmed that the dataset was complete with respect to missing-value entries.

Duplicate Record Analysis

Complete duplicate rows were checked using Pandas.

There were 0 completely duplicated rows.

The delivery_id column was then analyzed separately. There were 498 repeated delivery IDs, while the dataset contained 24,502 unique delivery IDs.

The repeated IDs were not automatically removed because a repeated delivery ID is different from an identical duplicate row. Removing these records without further investigation could result in the loss of potentially useful information.

Data Type and Format Cleaning

During the data inspection process, the columns delivery_time_hours and expected_time_hours were found to be stored in an unusual object/timestamp-like format.

Some values appeared in a format similar to:

1970-01-01 00:00:00.000000008

The values in this dataset represented encoded hour values. They were converted into numeric values suitable for analysis.

The conversion was performed using Pandas datetime processing and extraction of the nanosecond component.

After conversion, both time-related columns became integer-based numerical variables and were suitable for further preprocessing.

Outlier Detection

Outlier detection was performed using the Interquartile Range (IQR) method.

The following numerical variables were analyzed:

distance_km
package_weight_kg
delivery_time_hours
delivery_cost
Outlier Results
Variable	Potential Outliers
Distance	0
Package Weight	0
Delivery Time	203
Delivery Cost	0

The analysis identified 203 potential outliers in delivery time.

These observations were not automatically deleted. Further inspection suggested that longer delivery times could be realistic in logistics operations, particularly when deliveries involve longer distances or delays.

Therefore, the potential outliers were retained because there was not enough evidence to classify them as incorrect data-entry values.

This approach helped preserve potentially meaningful operational information.

Data Normalization

Data normalization was performed on important numerical variables using Min-Max normalization.

The following columns were normalized:

distance_km
package_weight_kg
delivery_time_hours
expected_time_hours
delivery_rating
delivery_cost

Min-Max normalization transforms numerical values into a common range from 0 to 1.

The general concept of Min-Max normalization is:

Normalized Value = (Value − Minimum Value) / (Maximum Value − Minimum Value)

Normalization is useful because numerical variables may have very different scales. For example, delivery cost may have much larger numerical values than a delivery rating. Scaling these variables to a common range makes them more suitable for many analytical and machine-learning techniques.

The original dataset was preserved, and a separate normalized dataset was created for comparison.

Normalization Results

After applying Min-Max normalization, the selected numerical variables were transformed to a range between 0 and 1.

The original delivery-cost values were also compared with their normalized values using a visualization.

The comparison is provided in:

delivery_cost_before_after.png

This visualization demonstrates the effect of normalization on the numerical scale of the delivery-cost variable.

Validation of the Preprocessed Dataset

After completing the preprocessing operations, the dataset was validated again.

The final validation produced the following results:

Missing values: 0
Complete duplicate rows: 0
Original dataset shape: 25,000 × 15
Normalized dataset shape: 25,000 × 15
delivery_time_hours type: int32
expected_time_hours type: int32
Normalized numerical variables: 0–1 range

The validation confirmed that the preprocessing process was completed without introducing new missing values or complete duplicate records.

Preprocessing Methodology

The overall preprocessing methodology followed a structured sequence:

Data Collection → Data Inspection → Data Quality Assessment → Missing Value Analysis → Duplicate Analysis → Data Type Cleaning → Outlier Detection → Outlier Evaluation → Normalization → Validation

Each step was performed to improve the reliability and usability of the dataset.

The process also emphasized that preprocessing decisions should be based on the characteristics of the data rather than automatically deleting unusual observations.

Tools and Technologies

The following tools and technologies were used:

Python 3.13.9
Pandas 2.3.3
Matplotlib
Scikit-learn
Visual Studio Code
GitHub
Project Files
week2_preprocessing.py

This Python script contains the preprocessing workflow used during Week 2. It covers dataset loading, inspection, missing-value checking, duplicate analysis, data-type conversion, outlier detection, normalization, validation, and visualization.

Week_2_Logistics_Data_Preprocessing_Report.docx

This document contains the detailed Week 2 internship report, including the methodology, data-quality findings, preprocessing decisions, code documentation, reflection, and conclusion.

delivery_cost_before_after.png

This visualization compares delivery-cost values before and after Min-Max normalization.

Key Learning Outcomes

This task provided practical experience in preparing a real-world-style logistics dataset for analysis.

The major learning outcomes were:

Understanding the importance of data preprocessing
Inspecting datasets before performing analysis
Identifying missing values
Identifying complete duplicate records
Investigating repeated identifiers
Handling unusual data formats
Detecting potential outliers using the IQR method
Evaluating whether outliers should be retained or removed
Applying Min-Max normalization
Validating the dataset after preprocessing
Documenting data-science workflows
Using visualizations to communicate preprocessing results
Reflection

This task helped me understand that data preprocessing is not simply about removing unusual or inconvenient data.

Each data-quality issue needs to be investigated before making a decision. For example, repeated delivery IDs were analyzed separately from complete duplicate records, and potential delivery-time outliers were retained because they could represent realistic logistics situations.

I also learned how important it is to preserve the original data while creating a processed version for analysis. This makes it easier to compare the original and transformed data and reduces the risk of permanently losing information.

The task improved my practical understanding of Python, Pandas, data cleaning, statistical outlier detection, normalization, and dataset validation.

Future Scope

The preprocessed logistics dataset can be used for further analysis such as:

Delivery delay analysis
Delivery cost analysis
Delivery partner performance analysis
Distance versus delivery-time analysis
Weather impact on delivery performance
Delivery rating analysis
Regional delivery performance analysis
Predictive analysis of delivery delays
Machine learning models for logistics optimization
Logistics performance dashboards
Conclusion

Week 2 successfully implemented a practical data preprocessing pipeline for the logistics dataset.

The dataset was inspected for quality issues, missing values and duplicates were analyzed, unusual time formats were converted into usable numerical values, potential outliers were identified and evaluated, and important numerical variables were normalized.

The final validation confirmed that the processed dataset remained complete and suitable for further analysis.

This preprocessing stage provides a reliable foundation for future logistics data analysis and machine-learning tasks.
