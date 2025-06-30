from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from tqdm import tqdm


class ParseDataAnalytics:
    def __init__(self, file: Path, words: list):
        print(f"Initializing ParseDataAnalytics with file: {file}")
        assert file.exists(), "File does not exist"
        data = pd.read_excel(file, index_col=0)
        self.data = data

        self.words = words
        # print(f"Data loaded successfully with shape: {self.data.shape}")
        # print(self.data.head(15))

    def reduce_media_names(self, df: pd.DataFrame):
        pattern = "El Mercurio"
        pmask = df["nombre_medio"].str.contains(pattern, case=False)
        print(f"Number of matches for {pattern} {pmask.sum()}")
        df.loc[pmask, "nombre_medio"] = pattern

        pattern = "La Tercera"
        pmask = df["nombre_medio"].str.contains(pattern, case=False)
        print(f"Number of matches for {pattern} {pmask.sum()}")
        df.loc[pmask, "nombre_medio"] = pattern

        pattern = "El Austral"
        pmask = df["nombre_medio"].str.contains(pattern, case=False)
        print(f"Number of matches for {pattern} {pmask.sum()}")
        df.loc[pmask, "nombre_medio"] = pattern

        pattern = "La Estrella"
        pmask = df["nombre_medio"].str.contains(pattern, case=False)
        print(f"Number of matches for {pattern} {pmask.sum()}")
        df.loc[pmask, "nombre_medio"] = pattern

        return df

    def reduce_media_names_top3(self, df: pd.DataFrame):
        # pattern = "El Mercurio"
        # pmask = df["nombre_medio"].str.contains(pattern, case=False)
        # print(f"Number of matches for {pattern} {pmask.sum()}")
        # df.loc[pmask, "nombre_medio"] = pattern

        category_counts = df["nombre_medio"].value_counts()
        ordered_categories = category_counts.index
        # print(ordered_categories)
        top_3 = ordered_categories[:3]
        # print(f"Top 3 media names: {top_3}")
        df = df[df["nombre_medio"].isin(top_3)]

        # exit(0)

        return df

    def reduce_media_sections(self, df: pd.DataFrame):
        df["seccion"] = df["seccion"].fillna("N/A")

        pattern = "Suplemento"
        pmask = df["seccion"].str.contains(pattern, case=False)
        print(f"Number of matches for {pattern} {pmask.sum()}")
        df.loc[pmask, "seccion"] = pattern

        pattern = "Reportaje"
        pmask = df["seccion"].str.contains(pattern, case=False)
        print(f"Number of matches for {pattern} {pmask.sum()}")
        df.loc[pmask, "seccion"] = pattern

        pattern = "Entrevista"
        pmask = df["seccion"].str.contains(pattern, case=False)
        print(f"Number of matches for {pattern} {pmask.sum()}")
        df.loc[pmask, "seccion"] = pattern

        pattern = "Patrimonio"
        pmask = df["seccion"].str.contains(pattern, case=False)
        print(f"Number of matches for {pattern} {pmask.sum()}")
        df.loc[pmask, "seccion"] = pattern

        return df

    def filter_media_by_type(self, media_type: int) -> pd.DataFrame:
        """Filters the DataFrame by the specified media type."""
        if media_type not in self.data["tipo_medio"].unique():
            raise ValueError(f"Media type '{media_type}' not found in data.")

        filtered_data = self.data[self.data["tipo_medio"] == media_type]
        print(
            f"Filtered data for media type '{media_type}' with shape: {filtered_data.shape}"
        )
        return filtered_data

    def high_impact_media(self):
        df = self.filter_media_by_type(7)
        df = self.reduce_media_names(df)
        df = self.reduce_media_sections(df)
        self.basic_analysis(df, Path("output/high_impact_media.png"))

    def medium_impact_media(self):
        df = self.filter_media_by_type(3)
        df = self.reduce_media_names(df)
        df = self.reduce_media_sections(df)
        self.basic_analysis(df, Path("output/medium_impact_media.png"))

    def low_impact_media(self):
        df = self.filter_media_by_type(0)
        df = self.reduce_media_names(df)
        df = self.reduce_media_sections(df)
        self.basic_analysis(df, Path("output/low_impact_media.png"))

    def plot_nombre_medios_histogram(self, df: pd.DataFrame, file: Path):

        plt.figure(figsize=(8, 8))  # Optional: adjust figure size
        # sns.histplot(data=df, x="nombre_medio", discrete=True, shrink=0.8)
        category_counts = df["nombre_medio"].value_counts()
        ordered_categories = category_counts.index
        sns.countplot(data=df, x="nombre_medio", order=ordered_categories)

        # Add title and labels for clarity
        plt.title("Distribución de nombres de medios")
        plt.xlabel("Nombre del Medio")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")  # ha='right' aligns labels nicely
        # plt.yticks(rotation=45, ha="right")  # ha='right' aligns labels nicely
        tmp = Path(str(file).replace(".png", "_hist.png"))
        plt.savefig(tmp)  # Saves as a PNG image
        plt.clf()  # Clear the current figure to avoid overlap in plots

    def plot_seccion_catplot(self, df: pd.DataFrame, file: Path):
        g = sns.catplot(data=df, x="seccion", y="nombre_medio")
        g.figure.set_size_inches(12, 6)  # Adjust the size of the figure
        plt.xticks(rotation=45, ha="right")  # ha='right' aligns labels nicely
        plt.yticks(rotation=45, ha="right")  # ha='right' aligns labels nicely
        # plt.show()
        tmp = Path(str(file).replace(".png", "_catplot.png"))
        plt.savefig(tmp, bbox_inches="tight")  # Saves as a PNG image
        plt.clf()  # Clear the current figure to avoid overlap in plots

    def plot_fecha_nombre_medio(self, df: pd.DataFrame, file: Path):
        col_list = [
            "nombre_medio",
            # "tipo_medio",
            # "seccion",
        ]
        for col in col_list:
            # Create the scatter plot
            plt.figure(figsize=(10, 6))  # Optional: Adjust figure size
            sns.scatterplot(x="fecha", y=col, data=df)

            # Optional: Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha="right")  # ha='right' aligns labels nicely

            # plt.title("Scatter Plot of Value over Time")
            plt.xlabel("Fecha")
            plt.ylabel(col.capitalize())
            plt.tight_layout()  # Adjust layout to prevent labels from overlapping
            # plt.show()
            assert file.suffix == ".png", "File must be a PNG image"
            assert file.parent.exists(), "File parent directory does not exist"
            tmp = Path(str(file).replace(".png", f"_fecha_{col}.png"))
            plt.savefig(tmp)  # Saves as a PNG image
            plt.clf()  # Clear the current figure to avoid overlap in plots

    def plot_fecha_sentimiento(self, df: pd.DataFrame, file: Path):
        col_list = [
            "sentiment",
            # "tipo_medio",
            # "seccion",
        ]
        for col in col_list:
            # Create the scatter plot
            plt.figure(figsize=(10, 6))  # Optional: Adjust figure size
            sns.scatterplot(x="fecha", y=col, data=df, hue="nombre_medio")

            # Optional: Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha="right")  # ha='right' aligns labels nicely

            # plt.title("Scatter Plot of Value over Time")
            plt.xlabel("Fecha")
            plt.ylabel(col.capitalize())
            plt.tight_layout()  # Adjust layout to prevent labels from overlapping]
            # pyplot.locator_params(axis="y", nbins=6)
            ax = plt.gca()
            ax.xaxis.set_major_locator(plt.MaxNLocator(10))
            # plt.show()
            assert file.suffix == ".png", "File must be a PNG image"
            assert file.parent.exists(), "File parent directory does not exist"
            tmp = Path(str(file).replace(".png", f"_fecha_{col}.png"))
            plt.savefig(tmp)  # Saves as a PNG image
            plt.clf()  # Clear the current figure to avoid overlap in plots

            # boxplot
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
            df.sort_values(by="fecha", ascending=False, inplace=True)
            df["week"] = df["fecha"].dt.isocalendar().week
            df["month"] = df["fecha"].dt.month
            # print(df["week"].value_counts())
            # sns.boxplot(x="fecha", y=col, data=df, hue="nombre_medio")
            # sns.boxplot(x="week", y=col, data=df, hue="nombre_medio")
            sns.boxplot(x="month", y=col, data=df, hue="nombre_medio")
            tmp = Path(str(file).replace(".png", f"_boxplot_fecha_{col}.png"))
            plt.savefig(tmp)
            plt.clf()  # Clear the current figure to avoid overlap in plots

            # boxplot by pattern
            for pattern in self.words:
                pmask = df["cuerpo"].str.contains(pattern, case=False, na=False)
                print(f"Number of matches for pattern '{pattern}': {pmask.sum()}")
                df_pattern = df[pmask]
                df_pattern["fecha"] = pd.to_datetime(
                    df_pattern["fecha"], errors="coerce"
                )
                df_pattern.sort_values(by="fecha", ascending=False, inplace=True)
                df_pattern["week"] = df_pattern["fecha"].dt.isocalendar().week
                df_pattern["month"] = df_pattern["fecha"].dt.month
                sns.boxplot(x="month", y=col, data=df_pattern, hue="nombre_medio")
                tmp = Path(
                    str(file).replace(".png", f"_boxplot_{pattern}_fecha_{col}.png")
                )
                plt.savefig(tmp)
                plt.clf()  # Clear the current figure to avoid overlap in plots

    def basic_analysis(self, df: pd.DataFrame, file: Path):
        # print(df["seccion"].unique())
        # print("-----------------")
        # print(df["nombre_medio"].value_counts().to_string())
        # print(df["tipo_medio"].value_counts().to_string())
        # print(df["seccion"].value_counts().to_string())

        self.plot_nombre_medios_histogram(df, file)
        # self.plot_fecha_nombre_medio(df, file)

        df = self.reduce_media_names_top3(df)

        self.plot_seccion_catplot(df, file)

        self.plot_fecha_nombre_medio(df, file)

        tmp = Path(str(file).replace(".png", "_dataframe.csv"))
        if not tmp.exists():
            print(f"Saving DataFrame to {tmp}")
            df = self.analyze_sentiment(df, file)
            df.to_csv(tmp, index=False)
        else:
            print(f"File {tmp} already exists. Skipping saving DataFrame.")
            df2 = pd.read_csv(tmp)
            # print(df2.head(10))
            # # df = self.data.merge(df2, on="id", how="left")
            # df = self.data.merge(df2, left_index=True, right_index=True, how="inner")
            # df["sentiment"] = df2["sentiment"]
            # print(df.head(10))
            # exit(0)
            df = df2

        self.plot_fecha_sentimiento(df, file)
        # return

        # plt.figure(figsize=(20, 10))  # Create a figure with a specific size
        # fig, ax = plt.subplots(figsize=(100, 60))  # Create a figure and axes
        # sns.set(rc={"figure.figsize": (20, 6)})  # Set default figure size

    def analyze_sentiment(self, df: pd.DataFrame, file: Path) -> pd.DataFrame:

        df = self.analyze_words(df, self.words)
        sentiment_list = []
        for inx, row in tqdm(
            df.iterrows(), total=df.shape[0], desc="Analyzing Sentiment"
        ):
            # print(f"Row {inx}: {row['cuerpo']}")
            sentiment = self.sentiment_analysis(row["cuerpo"])
            sentiment_list.append(sentiment)
            # print(f"Sentiment for row {inx}: {sentiment}")
        # print(df)

        df["sentiment"] = sentiment_list

        col = "sentiment"
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="nombre_medio", y=col, data=df)

        # Optional: Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha="right")  # ha='right' aligns labels nicely

        # plt.title("Scatter Plot of Value over Time")
        plt.xlabel("Fecha")
        plt.ylabel(col.capitalize())
        plt.tight_layout()  # Adjust layout to prevent labels from overlapping
        # plt.show()
        assert file.suffix == ".png", "File must be a PNG image"
        assert file.parent.exists(), "File parent directory does not exist"
        tmp = Path(str(file).replace(".png", f"_nombre_medio_{col}.png"))
        plt.savefig(tmp)  # Saves as a PNG image
        plt.clf()  # Clear the current figure to avoid overlap in plots

        return df

    def analyze_words(self, df: pd.DataFrame, words: list) -> pd.DataFrame:
        if not words:
            raise ValueError("No words provided for detection.")

        pattern = "|".join(words)
        pmask = df["cuerpo"].str.contains(pattern, case=False, na=False)
        print(f"Number of matches for pattern '{pattern}': {pmask.sum()}")
        return df[pmask]

    def sentiment_analysis(self, text: str) -> pd.DataFrame:
        # blob = TextBlob("I love this library", analyzer=NaiveBayesAnalyzer())
        blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
        # print(f"Sentiment: {blob.sentiment}")
        # print(f"p_pos: {blob.sentiment[1]}")
        return blob.sentiment[1]
        # df["sentiment"] = df["cuerpo"].apply(lambda x: TextBlob(x, analyzer=NaiveBayesAnalyzer()).sentiment)

    # def get_summary(self) -> pd.DataFrame:
    #     """Returns a summary of the DataFrame."""
    #     return self.data.describe()

    # def get_column_names(self) -> list:
    #     """Returns the names of the columns in the DataFrame."""
    #     return self.data.columns.tolist()

    # def get_shape(self) -> tuple:
    #     """Returns the shape of the DataFrame."""
    #     return self.data.shape
