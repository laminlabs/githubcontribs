import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def setup_svg_output():
    """Configure matplotlib to output SVG in Jupyter notebooks."""
    try:
        from IPython import get_ipython

        ipython = get_ipython()
        if ipython is not None:
            ipython.run_line_magic("config", "InlineBackend.figure_formats = ['svg']")
    except (ImportError, AttributeError):
        # Not in IPython/Jupyter environment, or magic not available
        pass


class Plotter:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        setup_svg_output()
        sns.set_theme()

    def plot_total_number_by_author(
        self, top_n: int = 10, exclude_author: str = "github-actions[bot]"
    ):
        """A vertical bar plot showing contribution types per author.

        Args:
            top_n: Number of top contributors to show. Defaults to 10.
            exclude_author: Author to exclude from the plot. Defaults to "github-actions[bot]".
        """
        df = self.df[self.df.author != exclude_author]

        commits_df: pd.DataFrame = df[df.type == "commit"]
        issues_df: pd.DataFrame = df[df.type == "issue"]
        prs_df: pd.DataFrame = df[df.type == "pr"]

        # Prepare the data
        contributors_data = pd.concat(
            [
                prs_df.groupby("author").size().rename("Pull requests"),
                commits_df.groupby("author").size().rename("Commits"),
                issues_df.groupby("author").size().rename("Issues"),
            ],
            axis=1,
        ).fillna(0)

        # Sort by total contributions and get top N
        contributors_data["Total"] = contributors_data.sum(axis=1)
        contributors_data = contributors_data.sort_values(
            "Total", ascending=False
        ).head(top_n)
        contributors_data = contributors_data.drop("Total", axis=1)

        # Reshape data for seaborn
        plot_data = contributors_data.reset_index().melt(
            id_vars="author", var_name="Activity Type", value_name="Count"
        )

        # Calculate date range from the dataframe
        min_date = pd.to_datetime(df["date"]).min()
        max_date = pd.to_datetime(df["date"]).max()
        date_range = (
            f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"
        )

        # Get all unique repositories
        repos = ", ".join(sorted(df["repo"].unique()))

        # Set up the plot style - adjusted figsize for vertical orientation
        plt.figure(figsize=(max(10, top_n * 0.8), 8))

        # Create the plot - changed to vertical orientation
        sns.barplot(
            data=plot_data,
            x="author",
            y="Count",
            hue="Activity Type",
            palette=["#2ecc71", "#3498db", "#e74c3c"],
            order=contributors_data.index,  # Maintain the sorted order
        )

        # Add value labels
        for c in plt.gca().containers:
            plt.gca().bar_label(c, label_type="edge", fmt="%d", padding=3)

        # Customize the plot with date range and repos in title
        plt.title(f"Contributions to repositories by author: {repos}\n{date_range}")
        plt.ylabel("Number of contributions")
        plt.xlabel("Author")

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha="right")

        # Position legend inside the canvas (upper right)
        plt.legend(loc="upper right")

        # Ensure all labels are visible
        plt.tight_layout()
