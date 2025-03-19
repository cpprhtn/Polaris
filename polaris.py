import polars as pl
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from io import StringIO
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class PolarisEDA:
    def __init__(self, file):
        file_content = StringIO(file.getvalue().decode("utf-8"))
        self.df = pl.read_csv(file_content, infer_schema_length=10000)

    def generate_eda_report(self):
        st.title("📊 Polaris EDA Report")
        st.write("### Comprehensive Exploratory Data Analysis Report")
        st.write("This report provides an in-depth analysis of the dataset, covering various statistical and visualization insights.")
        
        self.dataset_overview()
        self.detect_anomalies() 
        self.categorical_data_analysis()
        self.visualize_numeric_data()
        self.timeseries_analysis()
        self.analyze_binary_data()
        self.analyze_structured_data()
        self.correlation_matrix()
        self.feature_importance()
        self.cluster_analysis()
        self.pca_visualization()

    def dataset_overview(self):
        st.subheader("📌 Dataset Overview")
        st.write("Understanding the structure of the dataset helps to gain insights into the type and distribution of data.")
        st.write(f"🔹 Total Rows: {self.df.height}")
        st.write(f"🔹 Total Columns: {self.df.width}")
        st.write("🔹 Data Types:")
        st.dataframe(self.df.schema)
    
    def detect_anomalies(self):
        st.subheader("🚨 Anomaly Detection")
        st.write("Anomalies in the dataset can indicate potential data entry errors or extreme values that need attention.")
        numeric_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.Float64, pl.Int64]]

        if not numeric_cols:
            st.write("⚠️ No numeric columns for anomaly detection.")
            return

        # Isolation Forest for Numeric Outlier Detection
        model = IsolationForest(contamination=0.05, random_state=42)
        df_pd = self.df.select(numeric_cols).to_pandas()
        model.fit(df_pd)
        outliers = model.predict(df_pd)

        self.df = self.df.with_columns(pl.Series("outlier", outliers))

        outlier_count = (outliers == -1).sum()
        st.write(f"🔍 Detected {outlier_count} potential anomalies using Isolation Forest.")

        if outlier_count > 0:
            st.write("### 🚨 Outlier Summary")
            outlier_data = self.df.filter(self.df["outlier"] == -1)
            st.dataframe(outlier_data)

            st.write("### 📌 Anomaly Analysis Report")
            for col in numeric_cols:
                outlier_values = outlier_data[col].to_list()
                if outlier_values:
                    st.write(f"- **{col}** contains {len(outlier_values)} potential outliers. Example values: {outlier_values[:5]}")
            st.write("🔍 These anomalies might indicate data entry errors or unusual patterns.")
        else:
            st.write("✅ No significant anomalies detected.")

        # Detecting Invalid String Values
        st.subheader("🔍 Invalid String Values Detection")
        common_invalid_values = ["?", "unknown", "n/a", "null", "missing", "-", ""]

        text_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype == pl.Utf8]

        anomalies = []
        for col in text_cols:
            cleaned_col = self.df[col].cast(pl.Utf8).str.strip_chars().str.to_lowercase()
            invalid_counts = cleaned_col.is_in(common_invalid_values).sum()

            if invalid_counts > 0:
                detected_values = self.df[col].filter(cleaned_col.is_in(common_invalid_values)).unique().to_list()
                anomalies.append({
                    "Column": col,
                    "Invalid Values Count": invalid_counts,
                    "Detected Values": ", ".join(map(str, detected_values))
                })

        if anomalies:
            st.subheader("🔍 Detected Invalid String Values")
            st.table(anomalies)
            st.write("⚠️ The above values are commonly used to represent missing or incorrect data. Consider cleaning or replacing them appropriately.")
        else:
            st.write("✅ No invalid string values detected.")
    
    def visualize_numeric_data(self):
        st.subheader("📊 Numeric Data Distribution")
        st.write("The following histograms represent the distribution of numeric variables in the dataset.")
        numeric_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.Float64, pl.Int64]]
        
        for col in numeric_cols:
            st.write(f"🔹 **{col}**")
            fig, ax = plt.subplots(figsize=(4, 3))
            sns.histplot(self.df[col].to_pandas(), bins=20, kde=True, ax=ax)
            st.pyplot(fig)
            
    def analyze_binary_data(self):
        st.subheader("🔘 Binary Data Analysis")
        st.write("Binary data consists of values that can take only two unique states, typically 0/1 or True/False. Analyzing its distribution helps understand categorical distinctions.")
        
        binary_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype == pl.Boolean]
        
        if not binary_cols:
            st.write("⚠️ No binary columns detected.")
            return
        
        for col in binary_cols:
            st.write(f"🔹 **{col}**")
            value_counts = self.df[col].value_counts().to_pandas()
            st.bar_chart(value_counts.set_index(col))
            
            st.write("- The distribution of binary values in this column is displayed above.")
            st.write("- If a binary column is highly imbalanced, consider addressing class imbalance issues if used for classification.")
    
    def analyze_structured_data(self):
        st.subheader("📂 Structured Data Analysis (List/Struct)")
        st.write("Structured data includes list-type and structured columns that store nested values. Analyzing their usage can provide insights into hierarchical data.")
        
        structured_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.List, pl.Struct]]
        
        if not structured_cols:
            st.write("⚠️ No structured data columns detected.")
            return
        
        for col in structured_cols:
            st.write(f"🔹 **{col}**")
            st.write(f"- Example values: {self.df[col].head(5).to_list()}")
            st.write("- List columns store multiple values per row, whereas struct columns hold named subfields.")
            st.write("- Consider expanding or normalizing structured data for better interpretability.")

    
    def correlation_matrix(self):
        st.subheader("📈 Correlation Matrix")
        st.write("The heatmap below shows the correlation between numeric variables in the dataset.")
        numeric_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.Float64, pl.Int64]]
        
        if len(numeric_cols) < 2:
            st.write("⚠️ Not enough numeric columns for correlation matrix.")
            return

        corr_matrix = self.df.select(numeric_cols).to_pandas().corr()
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)
        
    def categorical_data_analysis(self):
        st.subheader("🔢 Categorical Data Analysis")
        st.write("Categorical variables contain discrete values that represent different categories or labels. Understanding their distribution helps identify dominant classes and potential imbalances.")
        
        cat_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype == pl.Utf8]
        
        if not cat_cols:
            st.write("⚠️ No categorical columns detected.")
            return
        
        for col in cat_cols:
            st.write(f"🔹 **{col}**")
            value_counts = self.df[col].value_counts().head(10).to_pandas()
            
            st.write(f"The top 10 most frequent values in `{col}` column are shown below.")
            st.bar_chart(value_counts.set_index(col))
            
            most_common = value_counts.iloc[0][col]
            st.write(f"- The most frequent value is `{most_common}`, appearing `{value_counts.iloc[0]['count']}` times.")
            st.write("- If a single category dominates, consider balancing the data to improve model performance in classification tasks.")
    
    def timeseries_analysis(self):
        st.subheader("📅 Time-Series Analysis")
        st.write("Time-series data consists of observations collected over time. Analyzing temporal trends can reveal seasonality, trends, and anomalies.")
        
        date_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype == pl.Date]
        
        if not date_cols:
            st.write("⚠️ No date columns detected.")
            return
        
        for col in date_cols:
            st.write(f"🔹 **{col}**")
            self.df = self.df.with_columns(self.df[col].cast(pl.Date))
            time_series = self.df.groupby(col).count()
            
            st.write(f"The time-series trend for `{col}` column is displayed below.")
            st.line_chart(time_series.to_pandas().set_index(col))
            
            st.write("- Peaks and dips in the time-series graph may indicate seasonality or external events affecting the data.")
            st.write("- If missing time periods exist, consider imputing missing values to maintain consistency.")
            
    def feature_importance(self):
        st.subheader("📌 Feature Importance (Random Forest)")
        st.write("Feature importance helps to identify which variables have the most impact on the target variable. This is useful for feature selection and understanding the predictive power of variables.")
        
        numeric_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.Float64, pl.Int64]]
        
        if len(numeric_cols) < 2:
            st.write("⚠️ Not enough numeric columns for feature importance analysis.")
            return
        
        X = self.df.select(numeric_cols[:-1]).to_pandas()
        y = self.df[numeric_cols[-1]].to_pandas()
        
        model = RandomForestRegressor() if y.dtype in ['float64', 'int64'] else RandomForestClassifier()
        model.fit(X, y)
        importance = model.feature_importances_
        
        st.write("The following bar chart represents the relative importance of each feature in predicting the target variable.")
        
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.barplot(x=numeric_cols[:-1], y=importance, ax=ax)
        ax.set_xticklabels(numeric_cols[:-1], rotation=45)
        st.pyplot(fig)
        
        most_important_feature = numeric_cols[np.argmax(importance)]
        least_important_feature = numeric_cols[np.argmin(importance)]
        
        st.write(f"- **{most_important_feature}** is the most influential feature in the model.")
        st.write(f"- **{least_important_feature}** has the least impact on predictions.")
        st.write("🔍 Consider removing features with low importance to simplify the model and improve efficiency.")
        
    def cluster_analysis(self):
        st.subheader("🔍 K-Means Clustering")
        st.write("Clustering is an unsupervised learning technique that groups similar data points together. It helps in identifying patterns and segmenting the dataset.")
        
        numeric_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.Float64, pl.Int64]]
        
        if len(numeric_cols) < 2:
            st.write("⚠️ Not enough numeric columns for clustering.")
            return
        
        X = self.df.select(numeric_cols).to_pandas()
        imputer = SimpleImputer(strategy='mean')
        X_imputed = imputer.fit_transform(X)
        
        kmeans = KMeans(n_clusters=3, random_state=42).fit(X_imputed)
        self.df = self.df.with_columns(pl.Series("cluster", kmeans.labels_))
        
        st.write("📊 Cluster Visualization")
        fig, ax = plt.subplots(figsize=(4, 3))
        scatter = ax.scatter(X_imputed[:, 0], X_imputed[:, 1], c=kmeans.labels_, cmap='viridis', alpha=0.6)
        ax.set_xlabel(numeric_cols[0])
        ax.set_ylabel(numeric_cols[1])
        plt.colorbar(scatter, label="Cluster")
        st.pyplot(fig)
        
        st.write("### 📌 Cluster Analysis Report")
        st.write("The dataset has been segmented into **3 clusters** using the K-Means algorithm. Each cluster represents a group of similar data points.")
        
        for i in range(3):
            cluster_size = (kmeans.labels_ == i).sum()
            st.write(f"- **Cluster {i}** contains {cluster_size} data points.")
        
        st.write("### 🔍 Key Observations")
        st.write("- Clusters are determined based on feature similarities.")
        st.write("- If clusters are overlapping, feature scaling or a different number of clusters may be needed.")
        st.write("- Further domain knowledge can help interpret the clusters for actionable insights.")
    
    def pca_visualization(self):
        st.subheader("📌 PCA Visualization")
        st.write("Principal Component Analysis (PCA) is used to reduce dimensionality while retaining important data patterns.")
        numeric_cols = [col for col, dtype in zip(self.df.columns, self.df.dtypes) if dtype in [pl.Float64, pl.Int64]]
        
        if len(numeric_cols) < 2:
            st.write("⚠️ Not enough numeric columns for PCA.")
            return
        
        X = self.df.select(numeric_cols).to_pandas()
        imputer = SimpleImputer(strategy='mean')
        X_imputed = imputer.fit_transform(X)
        
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(X_imputed)
        
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.scatter(reduced[:, 0], reduced[:, 1], alpha=0.5)
        ax.set_title("PCA Projection")
        st.pyplot(fig)
        
        explained_variance = pca.explained_variance_ratio_ * 100
        st.write(f"- **First Principal Component** explains {explained_variance[0]:.2f}% of the variance.")
        st.write(f"- **Second Principal Component** explains {explained_variance[1]:.2f}% of the variance.")
        st.write("🔍 PCA reduces dimensionality while retaining key patterns in data.")

class DataQuality:
    def __init__(self, df: pl.DataFrame):
        self.df = df

    def calculate_completeness(self) -> pl.DataFrame:
        return self.df.null_count() / len(self.df)

    def calculate_accuracy(self, column: str, valid_range: tuple) -> float:
        valid = self.df.with_columns((pl.col(column).is_between(valid_range[0], valid_range[1])).alias('valid'))
        return valid['valid'].mean()

    def calculate_timeliness(self, column: str, days_threshold: int = 7) -> float:
        if self.df[column].dtype == pl.Datetime:
            valid = self.df.with_columns((pl.col(column) > (datetime.now() - timedelta(days=days_threshold))).alias('valid'))
            return valid['valid'].mean()
        return np.nan

    def calculate_consistency(self, subset: list) -> float:
        return self.df.unique(subset=subset).height / self.df.height

    def calculate_uniqueness(self, column: str) -> float:
        return self.df[column].n_unique() / len(self.df)

    def assess_data_quality(self, accuracy_params: dict = {}, timeliness_column: str = None) -> pl.DataFrame:
        quality_metrics = {}
        quality_metrics['Completeness'] = self.calculate_completeness()
        
        for column, valid_range in accuracy_params.items():
            quality_metrics[f'Accuracy_{column}'] = self.calculate_accuracy(column, valid_range)

        if timeliness_column and timeliness_column in self.df.columns:
            quality_metrics['Timeliness'] = self.calculate_timeliness(timeliness_column)
        else:
            quality_metrics['Timeliness'] = np.nan

        quality_metrics['Consistency'] = self.calculate_consistency(self.df.columns)
        for column in self.df.columns:
            quality_metrics[f'Uniqueness_{column}'] = self.calculate_uniqueness(column)
        
        return pl.DataFrame(quality_metrics)

    def plot_quality_metrics(self, quality_metrics: pl.DataFrame):
        st.subheader("📊 Data Quality Metrics Overview")
        st.dataframe(quality_metrics)
        
        fig = make_subplots(rows=3, cols=2, subplot_titles=("Completeness", "Accuracy", "Timeliness", "Consistency", "Uniqueness"))
        
        metrics = ["Completeness", "Timeliness", "Consistency"]
        for i, metric in enumerate(metrics, 1):
            fig.add_trace(go.Bar(x=[metric], y=[quality_metrics[metric][0]], name=metric), row=(i+1)//2, col=(i%2)+1)
        
        st.plotly_chart(fig)