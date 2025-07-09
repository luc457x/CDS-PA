from .utils import *
from sklearn.neighbors import KNeighborsRegressor

def fill_nans_knn(df: pd.DataFrame, target_col: str, feature_cols: list, n_neighbors:5) -> pd.DataFrame:
    """
    Fill NaNs in the target column using K-Nearest Neighbors regression.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    target_col (str): The column with NaNs to be filled.
    feature_cols (list): The list of columns to be used as features for KNN.
    n_neighbors (int): The number of neighbors to use for KNN.

    Returns:
    pd.DataFrame: The DataFrame with NaNs filled in the target column.
    """
    # Create a mask for training data (where target is not NaN)
    train_mask = df[target_col].notna()

    # Split the data into training and prediction sets
    X_train = df.loc[train_mask, feature_cols]
    y_train = df.loc[train_mask, target_col]
    X_pred = df.loc[~train_mask, feature_cols]

    # Initialize and fit the KNeighborsRegressor
    knn_reg = KNeighborsRegressor(n_neighbors=n_neighbors)
    knn_reg.fit(X_train, y_train)

    # Predict the missing values
    df.loc[~train_mask, target_col] = knn_reg.predict(X_pred)

    return df
