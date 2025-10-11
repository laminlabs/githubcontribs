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

    def plot_contributor_activity(self, top_n: int = 10):
        """A horizontal bar plot showing contribution types per author.

        Args:
            top_n: Number of top contributors to show. Defaults to 10.
        """
        df = self.df

        commits_df: pd.DataFrame = df[df.type == "commit"]
        issues_df: pd.DataFrame = df[df.type == "issue"]
        prs_df: pd.DataFrame = df[df.type == "pr"]

        # Prepare the data
        contributors_data = pd.concat(
            [
                commits_df.groupby("author").size().rename("Commits"),
                issues_df.groupby("author").size().rename("Issues"),
                prs_df.groupby("author").size().rename("Pull Requests"),
            ],
            axis=1,
        ).fillna(0)

        # Sort by total contributions and get top N
        contributors_data["Total"] = contributors_data.sum(axis=1)
        contributors_data = contributors_data.sort_values("Total", ascending=True).tail(
            top_n
        )
        contributors_data = contributors_data.drop("Total", axis=1)

        # Reshape data for seaborn
        plot_data = contributors_data.reset_index().melt(
            id_vars="author", var_name="Activity Type", value_name="Count"
        )

        # Set up the plot style
        plt.figure(figsize=(12, max(8, top_n * 0.5)))

        # Create the plot
        sns.barplot(
            data=plot_data,
            y="author",
            x="Count",
            hue="Activity Type",
            palette=["#2ecc71", "#3498db", "#e74c3c"],
            orient="h",
        )

        # Add value labels
        for c in plt.gca().containers:
            plt.gca().bar_label(c, label_type="center", fmt="%d")

        # Customize the plot
        plt.title("Contribution Types by Author")
        plt.xlabel("Number of Contributions")
        plt.ylabel("Author")

        # Adjust legend position
        plt.legend(bbox_to_anchor=(1, 1.02), loc="upper left")

        # Ensure all labels are visible
        plt.tight_layout()

        # No need to return anything - plot is displayed in notebook
