#Import ProcessGameState.py
from ProcessGameState import ProcessGameState

#Numpy and Pandas for Data Processing
import numpy as np
import pandas as pd

#Import matplotlib and required libraries
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Polygon

#Heatmap Density Legend
from matplotlib.colorbar import ColorbarBase
from matplotlib.cm import ScalarMappable
import matplotlib.colors as mcolors

#Seaborn for Heatmap
import seaborn as sns


def commonStrategyQuestion():
    """
    Calls functions in ProcessGameState.py to answer: "Is entering via the light blue boundary a common strategy used by Team2 on T (terrorist) side?"
    """
    # Get a copy of DataFrame
    dataFrameTeam2T = gameStateProcessor.getDataFrame()

    # Filter DataFrame by Team2 and T side
    dataFrameTeam2T = gameStateProcessor.filterByTeamAndSide(dataFrameTeam2T, team='Team2', side='T')

    # Filter DataFrame by light blue boundary
    enteringInformation = gameStateProcessor.enteringBoundaryPerRound(dataFrameTeam2T)
    print('-------------')
    print("Is entering via the light blue boundary a common strategy used by Team2 on T (terrorist) side?")
    print('-------------')
    print(
        f"> Result: Percentage of times Team2 on T side enters the light blue boundary: {enteringInformation['percentage']}%.")
    print('-------------')
    print("Round | Entered")
    print('-------------')
    print(enteringInformation['rounds'])
    return

#2b
def averageTimerQuestion():
    """
    Calls functions in ProcessGameState.py to answer: "What is the average timer that Team2 on T (terrorist) side enters 'BombsiteB' with least 2 rifles or SMGs?"
    """
    print('-------------')
    print("What is the average timer that Team2 on T (terrorist) side enters 'BombsiteB' with least 2 rifles or SMGs?")

    # Select for Rifle and SMG
    relevantWeapons = ['Rifle', 'SMG']

    # Get a copy of DataFrame
    dataFrameTeam2T = gameStateProcessor.getDataFrame()

    # Filter DataFrame by Team2 and T side
    dataFrameTeam2T = gameStateProcessor.filterByTeamAndSide(dataFrameTeam2T, team='Team2', side='T')

    # Filter DataFrame by area_name = "BombSiteB"
    dataFrameTeam2T = gameStateProcessor.filterByAreaName(dataFrameTeam2T, "BombsiteB")

    # Calculate rounds and average seconds
    enteringInformation = gameStateProcessor.enteringWithMinCountWeapons(dataFrameTeam2T, relevantWeapons, 2)

    if len(enteringInformation) == 0:
        print('-------------')
        print("Result: In the provided data, Team2 on T side never enters “BombsiteB” with at least 2 rifles or SMGs.")
        return
    
    averageTimer = enteringInformation['average_seconds'].mean()
    print(f"Overall average timer: {averageTimer} seconds")
    print('-------------')
    print("Round | Average Timer")
    print('-------------')
    for index, row in enteringInformation.iterrows():
        print(f"{row['round_num']} | {row['average_seconds']} seconds")
  
    return

#2c
def heatMapQuestion():
    """
    Generates Heatmap to answer: "Now that we've gathered data on Team2 T side, let's examine their CT (counter-terrorist) Side. Using the same data
    set, tell our coaching staff where you suspect them to be waiting inside "BombsiteB."
    """
    # Create a copy of the DataFrame
    dataFrame = gameStateProcessor.getDataFrame()

    # Filter DataFrame by Team2 and CT side
    filteredDataFrame = gameStateProcessor.filterByTeamAndSide(dataFrame, team='Team2', side='CT')

    # Filter DataFrame by area_name = "BombSiteB"
    filteredDataFrame = gameStateProcessor.filterByAreaName(filteredDataFrame, "BombsiteB")

    # Load the image to matplotlib
    image =  plt.imread('data/de_overpass_radar.jpeg')

    # Create figure and axes
    fig, ax = plt.subplots()

    # Plot the image
    ax.imshow(image)

    # Normalize the xy values of dataframe to overlay data points to image (1024x1024), but (770x1011) for radar image
    # 1. Shift the xy values so that min values are 0. Also flip Y values due to inverted y-axis between image and coordinate system
    # 2. Divide to scale the range of values to be between 0 and 1
    # 3. Multiply the range of values to match new scale
    # 4. Due to black borders around radar, add 160 to x and 13 to y to center the heatmap
    normalizedX = ((filteredDataFrame['x'] - dataFrame['x'].min()) / (dataFrame['x'].max() - dataFrame['x'].min())) * 770 + 160
    normalizedY = ((dataFrame['y'].max() - filteredDataFrame['y']) / (dataFrame['y'].max() - dataFrame['y'].min())) * 1011 + 13

    # The df x and y coordinates are in pixels, need to convert to same scale as the image
    ax.set_xlim(0, 1024)
    ax.set_ylim(1024, 0)

    # Create a DataFrame for the normalized x and y values
    df_normalized = pd.DataFrame({'x': normalizedX, 'y': normalizedY})

    # Define color legend for heatmap using matplotlib colormap
    cmap = matplotlib.colormaps.get_cmap('hot')

    # Using seaborn KDEplot to generate heat map
    sns.kdeplot(data=df_normalized, x='x', y='y', cmap=cmap, fill=True, ax=ax, thresh=0, alpha=0.7)

    # Create color legend
    sm = ScalarMappable(cmap=cmap)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, orientation='vertical', label='Density')

    # Show the plot
    plt.show()

#Light Blue Boundary Polygon
polygon = [(-1735, 250), (-2024, 398), (-2806, 742),
           (-2472, 1233), (-1565, 580)]

z_min = 285
z_max = 421

data_path = 'data/game_state_frame_data.parquet'

#Initial Data Processing for Light Blue Boundary
gameStateProcessor = ProcessGameState(polygon, z_min, z_max, data_path)
gameStateProcessor.loadData()
gameStateProcessor.processBoundaryChecks()
gameStateProcessor.processWeaponExtraction()

# Question 2a
commonStrategyQuestion()

# Question 2b
averageTimerQuestion()

# Question 2c
heatMapQuestion()




