import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def encode_categorical_columns(input_df, columns_to_encode):
    """
    Encode categorical columns in a DataFrame using OneHotEncoder.

    Parameters:
    - input_df (pd.DataFrame): The input DataFrame containing categorical columns.
    - columns_to_encode (list): List of column names to be one-hot encoded.

    Returns:
    - encoded_df (pd.DataFrame): The DataFrame with categorical columns one-hot encoded.
    """

    # Extract the columns to encode
    data_to_encode = input_df[columns_to_encode]

    # Initialize the OneHotEncoder with drop='if_binary'
    encoder = OneHotEncoder(drop='if_binary')

    # Fit and transform the data
    encoded_data = encoder.fit_transform(data_to_encode)

    # Convert the encoded data to a DataFrame
    encoded_df = pd.DataFrame(encoded_data.toarray(),
                              columns=encoder.get_feature_names_out(columns_to_encode))

    # Concatenate the encoded DataFrame with the original DataFrame
    result_df = pd.concat([input_df, encoded_df], axis=1)

    # Drop the original categorical columns
    result_df.drop(columns=columns_to_encode, inplace=True)

    return result_df
