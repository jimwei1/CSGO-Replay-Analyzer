# Import pandas and json for ETL process
import pandas
import json
import matplotlib.path
import numpy as np

class ProcessGameState:
    def __init__(self, polygon, z_min, z_max, data_path):
        self.polygon = matplotlib.path.Path(polygon, closed=False)
        self.z_min = z_min
        self.z_max = z_max
        self.data_path = data_path
        self.df = None

    def loadData(self):
        """
        Load data from parquet file into pandas DataFrame.
        """
        self.df = pandas.read_parquet(self.data_path)
        return self.df

    def getDataFrame(self):
        """
        Get a copy of the DataFrame.
        """
        return self.df.copy()

    def checkCoordinates(self, x, y, z):
        """
        Check if the given x,y,z coordinates are within the defined polygon boundaries and z-axis range, return boolean.
        """
        if not (self.z_min <= z <= self.z_max):
            return False
        
        return self.polygon.contains_point((x, y))

    def extractWeaponClasses(self, inventory):
        """
        Extract weapon classes from the inventory list.
        """
        try:
            if inventory is None:
                return []

            weaponClasses = []

            for item in inventory:
                if 'weapon_class' in item:
                    weaponClasses.append(item['weapon_class'])
            return weaponClasses
        
        except (json.JSONDecodeError, KeyError, TypeError):
            return []

    def processBoundaryChecks(self):
        """
        Process boundary checks for all rows in the DataFrame and add a new column 'within_boundary' indicating if the coordinates are within the boundary.
        """
        self.df['within_boundary'] = self.df.apply(
            lambda row: self.checkCoordinates(
                row['x'], row['y'], row['z']),
            axis='columns'
        )

        return self.df

    def processWeaponExtraction(self):
        """
        Process weapon extraction for all rows in the DataFrame and update the 'inventory' column with the extracted weapon classes.
        """
        self.df['inventory'] = self.df['inventory'].apply(
            self.extractWeaponClasses)
        
        return self.df

    def filterByTeamAndSide(self, dataframe, team, side):
        """
        Filter the DataFrame based on the given team and side.
        """
        return dataframe[(dataframe['team'] == team) & (dataframe['side'] == side)]

    def filterByBoundary(self, dataframe, boundary):
        """
        Filter the DataFrame based on the within_boundary column.
        """
        return dataframe[(dataframe['within_boundary'] == boundary)]

    def filterByMinCountWeapons(self, dataframe, weapons, count):
        """
        Filter the DataFrame based on min count of selected weapons by caculating number of selected weapons in inventory and compare with count
        """
        return dataframe[(dataframe['inventory'].apply(lambda x: sum(1 for item in x if item in weapons) if isinstance(x, list) else 0) >= count)]


    def enteringWithMinCountWeapons(self, dataframe, weapons, count):
        """
        Filter the DataFrame based on the minimum count of matching weapons in the inventory per round,
        and calculate the aggregated statistics for the filtered rounds.
        """

        # Only count each player once per round
        df = dataframe.drop_duplicates(subset=['round_num', 'player']).copy()

        # Count the number of matching weapons in each player's inventory by creating new column 'matching_weapon_count'
        # which counts num of weapons in inventory that are in the weapons list
        df.loc[:, 'matching_weapon_count'] = df['inventory'].apply(
            lambda x: sum(item in weapons for item in x) if isinstance(
                x, list) else 0
        )

        # Remove rows in DataFrame where matching_weapon_count is 0
        df = df[df['matching_weapon_count'] > 0].copy()

        # Group DataFrame by round_num and aggregate the matching_weapon_count and seconds columns
        df = df.groupby('round_num').agg({
            'matching_weapon_count': 'sum',
            'seconds': 'sum'
        }).reset_index()

        # Create new column 'average_seconds' which is the seconds column divided by the matching_weapon_count column
        # as seconds is aggregate time of all players, while matching_weapon_count is num of players
        df.loc[:, 'average_seconds'] = df['seconds'] / \
            df['matching_weapon_count']

        # Return rows where matching_weapon_count is greater than or equal to count
        return df.loc[df['matching_weapon_count'] >= count]

    def enteringBoundaryPerRound(self, dataframe):
        """
        Calculate the number of rounds and percentage of rounds where at least one player entered the boundary.
        """

        # If empty DataFrame, return 0
        if (len(dataframe) == 0):
            return 0

        # Group DataFrame by round_num and check if any player entered the boundary per round
        roundsWithinBoundary = dataframe.groupby(
            'round_num')['within_boundary'].any()

        # Return num of rounds and percentage of rounds where player is within boundary
        return {
            'rounds': roundsWithinBoundary,
            'percentage': roundsWithinBoundary.sum() / len(roundsWithinBoundary) * 100
        }

    def filterByAreaName(self, dataframe, area_name):
        """
        Filter the DataFrame based on the area_name column.
        """
        return dataframe[(dataframe['area_name'] == area_name)]

    def averageTimerPerRound(self, dataframe):
        """
        Calculate the average timer per round and overall average timer.
        """
        # If empty database, return 0
        if (len(dataframe) == 0):
            print("No data")

        # Group DataFrame by round_num and calculate the mean of the seconds column
        timer = dataframe.groupby('round_num')['seconds'].mean()

        # Return average timer per round and overall average timer
        return{
            'rounds': timer,
            'overall_average': timer.mean()
        }

    # def create_transformation(pixel_points, xy_points):
    #     """
    #         Create a transformation function that maps pixel coordinates to XY coordinates based on a linear regression model.
    #     """
    #     xy_points = np.array(xy_points)  # Convert to numpy array
    #     x_model = LinearRegression().fit(pixel_points, xy_points[:, 0])
    #     y_model = LinearRegression().fit(pixel_points, xy_points[:, 1])

    #     def transform(pixel_point):
    #         return [x_model.predict([pixel_point])[0], y_model.predict([pixel_point])[0]]

    #     return transform
