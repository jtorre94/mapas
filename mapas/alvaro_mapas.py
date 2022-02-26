import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans


def cluster_coordinates(
        df: pd.DataFrame,
        n_clusters: int = 5
) -> pd.DataFrame:
    """ Groups the GPS coordinates into n clusters.

    :param df: input dataframe with GPS coordinates.
    :type df: pd.DataFrame
    :param n_clusters:
    :type n_clusters: int
    :return: input dataframe with extra column with the groups.
    :rtype: pd.DataFrame
    """

    df = df.copy()

    df_cols = df[['LATITUD', 'LONGITUD']]

    kmeans = KMeans(n_clusters=n_clusters, init='k-means++')
    kmeans.fit(df_cols)  # Compute k-means clustering.
    df['GRUPO'] = kmeans.fit_predict(df_cols)
    # centers = kmeans.cluster_centers_  # Coordinates of cluster centers.
    # labels = kmeans.predict(df_cols)  # Labels of each point

    return df


def plot_map(df: pd.DataFrame) -> None:
    """ Plots GPS into World Map.

    :param df: clustered dataframe.
    :type df: pd.DataFrame
    :return: side effect: shows the clustered points in the map.
    :rtype: None
    """

    fig = px.scatter_geo(
        df,
        lat='LATITUD',
        lon='LONGITUD',
        hover_name="NOMBRE",
        color='GRUPO'
    )
    fig.update_layout(title='World map', title_x=0.5)
    fig.show()


def main():
    df = pd.read_csv('mydata.csv')
    df = cluster_coordinates(df)
    plot_map(df)


if __name__ == '__main__':
    main()
