# 1.0 Imports


```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from nbconvert import MarkdownExporter
from nbformat import read, write
import os
```

# 2.0 Set Globals & Functions


```python
def checkData(x):
    print(f"\nInfo dos valores:\n")
    print(x.info())
    print(f"\nDescrição dos dados:\n\n{x.describe()}")
    return

def checkNaN(x):
    # Recebe um DataFrame e retorna a quantidade de valores nulos e não nulos.
    null_count = x.isna().sum()
    non_null_count = x.notnull().sum()
    print(f"Null values:\n {null_count}")
    print(f"Non-null values:\n {non_null_count}")
    return

def checkOutliers(x):
    """Recebe um DataFrame e retorna um DataFrame com os outliers.
    Baseia-se no pressuposto de que os dados estão normalmente distribuídos."""
    dfOutliers  = pd.DataFrame()
    # Itera sobre as colunas númericas
    for column in x.select_dtypes(include=[np.number]).columns:
        # Calcula o 1 quartil (Q1)
        Q1 = x[column].quantile(0.25)
        # Calcula o 3 quartil (Q3)
        Q3 = x[column].quantile(0.75)
        # Calcula o Intervalo Interquartil (IQR)
        IQR = Q3 - Q1
        # Define os limites inferior e superior para outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        # Identica os outliers da coluna atual e adiciona ao DataFrame de outliers
        outliers = x[(x[column] < lower_bound) | (x[column] > upper_bound)]
        # Concatene os outliers da coluna atual ao DataFrame de outliers
        dfOutliers = pd.concat([dfOutliers, outliers])
    outliersData = dfOutliers.drop_duplicates().reset_index(drop=True)
    return outliersData

def corr(x):
    plt.figure(figsize=(10,8))
    sns.heatmap(x.select_dtypes(include=[np.number]).corr(), annot=True)
    plt.show()
    return

def hist(x):
    # Recebe um DataFrame e plota um histograma para cada coluna numérica.
    x.hist(bins=50, figsize=(25,10))
    plt.show()
    return



```

# 3.0 Carregamento e Checagem


```python
df_raw = pd.read_csv("train.csv")
```


```python
checkData(df_raw)
```

    
    Info dos valores:
    
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4467 entries, 0 to 4466
    Data columns (total 20 columns):
     #   Column                       Non-Null Count  Dtype  
    ---  ------                       --------------  -----  
     0   ID                           4467 non-null   object 
     1   Delivery_person_ID           4467 non-null   object 
     2   Delivery_person_Age          4467 non-null   object 
     3   Delivery_person_Ratings      4467 non-null   object 
     4   Restaurant_latitude          4467 non-null   float64
     5   Restaurant_longitude         4467 non-null   float64
     6   Delivery_location_latitude   4467 non-null   float64
     7   Delivery_location_longitude  4467 non-null   float64
     8   Order_Date                   4467 non-null   object 
     9   Time_Orderd                  4467 non-null   object 
     10  Time_Order_picked            4467 non-null   object 
     11  Weatherconditions            4467 non-null   object 
     12  Road_traffic_density         4467 non-null   object 
     13  Vehicle_condition            4467 non-null   int64  
     14  Type_of_order                4467 non-null   object 
     15  Type_of_vehicle              4467 non-null   object 
     16  multiple_deliveries          4467 non-null   object 
     17  Festival                     4467 non-null   object 
     18  City                         4466 non-null   object 
     19  Time_taken(min)              4466 non-null   object 
    dtypes: float64(4), int64(1), object(15)
    memory usage: 698.1+ KB
    None
    
    Descrição dos dados:
    
           Restaurant_latitude  Restaurant_longitude  Delivery_location_latitude  \
    count          4467.000000           4467.000000                 4467.000000   
    mean             16.873720             69.855186                   17.345751   
    std               8.320083             23.490634                    7.436276   
    min             -30.902872            -88.322337                    0.010000   
    25%              12.906229             73.170000                   12.969496   
    50%              18.546258             75.894377                   18.619299   
    75%              22.725835             78.013330                   22.781857   
    max              30.914057             88.433452                   31.035562   
    
           Delivery_location_longitude  Vehicle_condition  
    count                  4467.000000        4467.000000  
    mean                     70.509414           1.022386  
    std                      21.655254           0.840340  
    min                       0.010000           0.000000  
    25%                      73.280937           0.000000  
    50%                      75.996362           1.000000  
    75%                      78.081576           2.000000  
    max                      88.563452           3.000000  
    


```python
df_raw.sample(30)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID</th>
      <th>Delivery_person_ID</th>
      <th>Delivery_person_Age</th>
      <th>Delivery_person_Ratings</th>
      <th>Restaurant_latitude</th>
      <th>Restaurant_longitude</th>
      <th>Delivery_location_latitude</th>
      <th>Delivery_location_longitude</th>
      <th>Order_Date</th>
      <th>Time_Orderd</th>
      <th>Time_Order_picked</th>
      <th>Weatherconditions</th>
      <th>Road_traffic_density</th>
      <th>Vehicle_condition</th>
      <th>Type_of_order</th>
      <th>Type_of_vehicle</th>
      <th>multiple_deliveries</th>
      <th>Festival</th>
      <th>City</th>
      <th>Time_taken(min)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4344</th>
      <td>0x67a1</td>
      <td>BANGRES15DEL03</td>
      <td>23</td>
      <td>4.7</td>
      <td>12.975377</td>
      <td>77.696664</td>
      <td>13.035377</td>
      <td>77.756664</td>
      <td>21-03-2022</td>
      <td>20:55:00</td>
      <td>21:10:00</td>
      <td>conditions Windy</td>
      <td>Jam</td>
      <td>2</td>
      <td>Buffet</td>
      <td>scooter</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 28</td>
    </tr>
    <tr>
      <th>2377</th>
      <td>0x4ab3</td>
      <td>JAPRES08DEL02</td>
      <td>36</td>
      <td>4.4</td>
      <td>26.910262</td>
      <td>75.783013</td>
      <td>26.990262</td>
      <td>75.863013</td>
      <td>18-03-2022</td>
      <td>18:00:00</td>
      <td>18:05:00</td>
      <td>conditions Fog</td>
      <td>Medium</td>
      <td>1</td>
      <td>Buffet</td>
      <td>scooter</td>
      <td>0</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 43</td>
    </tr>
    <tr>
      <th>2949</th>
      <td>0x8728</td>
      <td>PUNERES16DEL03</td>
      <td>37</td>
      <td>4.7</td>
      <td>18.536718</td>
      <td>73.830327</td>
      <td>18.566719</td>
      <td>73.860327</td>
      <td>07-03-2022</td>
      <td>19:55:00</td>
      <td>20:10:00</td>
      <td>conditions Windy</td>
      <td>Jam</td>
      <td>2</td>
      <td>Snack</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 25</td>
    </tr>
    <tr>
      <th>1394</th>
      <td>0x131b</td>
      <td>COIMBRES06DEL01</td>
      <td>20</td>
      <td>4.3</td>
      <td>11.021278</td>
      <td>76.995017</td>
      <td>11.031278</td>
      <td>77.005017</td>
      <td>26-03-2022</td>
      <td>08:20:00</td>
      <td>08:25:00</td>
      <td>conditions Stormy</td>
      <td>Low</td>
      <td>0</td>
      <td>Drinks</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 24</td>
    </tr>
    <tr>
      <th>4329</th>
      <td>0xdc56</td>
      <td>LUDHRES06DEL03</td>
      <td>29</td>
      <td>4.8</td>
      <td>30.895204</td>
      <td>75.822103</td>
      <td>30.985204</td>
      <td>75.912103</td>
      <td>18-02-2022</td>
      <td>23:40:00</td>
      <td>23:50:00</td>
      <td>conditions Stormy</td>
      <td>Low</td>
      <td>1</td>
      <td>Meal</td>
      <td>scooter</td>
      <td>0</td>
      <td>No</td>
      <td>Urban</td>
      <td>(min) 17</td>
    </tr>
    <tr>
      <th>1459</th>
      <td>0x552f</td>
      <td>PUNERES17DEL02</td>
      <td>26</td>
      <td>5</td>
      <td>18.530963</td>
      <td>73.828972</td>
      <td>18.660963</td>
      <td>73.958972</td>
      <td>27-03-2022</td>
      <td>17:45:00</td>
      <td>17:50:00</td>
      <td>conditions Stormy</td>
      <td>Medium</td>
      <td>1</td>
      <td>Buffet</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 21</td>
    </tr>
    <tr>
      <th>3078</th>
      <td>0x6538</td>
      <td>VADRES010DEL03</td>
      <td>36</td>
      <td>4.4</td>
      <td>22.310329</td>
      <td>73.169083</td>
      <td>22.340329</td>
      <td>73.199083</td>
      <td>19-03-2022</td>
      <td>19:20:00</td>
      <td>19:25:00</td>
      <td>conditions Sandstorms</td>
      <td>Jam</td>
      <td>0</td>
      <td>Snack</td>
      <td>motorcycle</td>
      <td>0</td>
      <td>No</td>
      <td>Semi-Urban</td>
      <td>(min) 48</td>
    </tr>
    <tr>
      <th>2967</th>
      <td>0xaad4</td>
      <td>MYSRES15DEL03</td>
      <td>25</td>
      <td>4.8</td>
      <td>12.352058</td>
      <td>76.606650</td>
      <td>12.442058</td>
      <td>76.696650</td>
      <td>16-03-2022</td>
      <td>18:45:00</td>
      <td>19:00:00</td>
      <td>conditions Cloudy</td>
      <td>Medium</td>
      <td>0</td>
      <td>Snack</td>
      <td>motorcycle</td>
      <td>2</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 38</td>
    </tr>
    <tr>
      <th>106</th>
      <td>0x9f99</td>
      <td>MUMRES11DEL01</td>
      <td>23</td>
      <td>4.8</td>
      <td>18.994237</td>
      <td>72.825553</td>
      <td>19.104237</td>
      <td>72.935553</td>
      <td>18-03-2022</td>
      <td>22:35:00</td>
      <td>22:40:00</td>
      <td>conditions Cloudy</td>
      <td>Low</td>
      <td>2</td>
      <td>Snack</td>
      <td>scooter</td>
      <td>1</td>
      <td>No</td>
      <td>Urban</td>
      <td>(min) 22</td>
    </tr>
    <tr>
      <th>496</th>
      <td>0x9155</td>
      <td>INDORES05DEL02</td>
      <td>26</td>
      <td>4.8</td>
      <td>22.727021</td>
      <td>75.884167</td>
      <td>22.747021</td>
      <td>75.904167</td>
      <td>26-03-2022</td>
      <td>09:50:00</td>
      <td>10:00:00</td>
      <td>conditions Windy</td>
      <td>Low</td>
      <td>2</td>
      <td>Buffet</td>
      <td>scooter</td>
      <td>0</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 14</td>
    </tr>
    <tr>
      <th>2158</th>
      <td>0x506e</td>
      <td>BANGRES04DEL01</td>
      <td>24</td>
      <td>4.6</td>
      <td>12.980410</td>
      <td>77.640489</td>
      <td>13.090410</td>
      <td>77.750489</td>
      <td>14-03-2022</td>
      <td>20:10:00</td>
      <td>20:25:00</td>
      <td>conditions Sunny</td>
      <td>Jam</td>
      <td>1</td>
      <td>Meal</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 23</td>
    </tr>
    <tr>
      <th>3769</th>
      <td>0x152e</td>
      <td>VADRES02DEL02</td>
      <td>25</td>
      <td>5</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.130000</td>
      <td>0.130000</td>
      <td>02-03-2022</td>
      <td>19:50:00</td>
      <td>20:00:00</td>
      <td>conditions Stormy</td>
      <td>Jam</td>
      <td>1</td>
      <td>Snack</td>
      <td>scooter</td>
      <td>1</td>
      <td>No</td>
      <td>Urban</td>
      <td>(min) 27</td>
    </tr>
    <tr>
      <th>1789</th>
      <td>0x6343</td>
      <td>COIMBRES02DEL01</td>
      <td>25</td>
      <td>5</td>
      <td>11.022477</td>
      <td>76.995667</td>
      <td>11.132477</td>
      <td>77.105667</td>
      <td>29-03-2022</td>
      <td>18:15:00</td>
      <td>18:25:00</td>
      <td>conditions Sandstorms</td>
      <td>Medium</td>
      <td>2</td>
      <td>Snack</td>
      <td>scooter</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 18</td>
    </tr>
    <tr>
      <th>292</th>
      <td>0x8de9</td>
      <td>SURRES14DEL03</td>
      <td>21</td>
      <td>4.9</td>
      <td>21.157729</td>
      <td>72.768726</td>
      <td>21.247729</td>
      <td>72.858726</td>
      <td>20-03-2022</td>
      <td>23:20:00</td>
      <td>23:30:00</td>
      <td>conditions Fog</td>
      <td>Low</td>
      <td>2</td>
      <td>Buffet</td>
      <td>scooter</td>
      <td>1</td>
      <td>No</td>
      <td>NaN</td>
      <td>(min) 21</td>
    </tr>
    <tr>
      <th>1463</th>
      <td>0xb752</td>
      <td>INDORES09DEL03</td>
      <td>25</td>
      <td>4.8</td>
      <td>22.725835</td>
      <td>75.887648</td>
      <td>22.755835</td>
      <td>75.917648</td>
      <td>05-03-2022</td>
      <td>21:50:00</td>
      <td>22:00:00</td>
      <td>conditions Cloudy</td>
      <td>Jam</td>
      <td>0</td>
      <td>Meal</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 26</td>
    </tr>
    <tr>
      <th>3475</th>
      <td>0x4a92</td>
      <td>PUNERES14DEL02</td>
      <td>33</td>
      <td>4.1</td>
      <td>18.516216</td>
      <td>73.842527</td>
      <td>18.646216</td>
      <td>73.972527</td>
      <td>04-04-2022</td>
      <td>18:20:00</td>
      <td>18:35:00</td>
      <td>conditions Stormy</td>
      <td>Medium</td>
      <td>0</td>
      <td>Buffet</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 43</td>
    </tr>
    <tr>
      <th>2184</th>
      <td>0x7890</td>
      <td>SURRES02DEL02</td>
      <td>26</td>
      <td>5</td>
      <td>21.186608</td>
      <td>72.794136</td>
      <td>21.236608</td>
      <td>72.844136</td>
      <td>15-03-2022</td>
      <td>17:35:00</td>
      <td>17:50:00</td>
      <td>conditions Stormy</td>
      <td>Medium</td>
      <td>2</td>
      <td>Meal</td>
      <td>electric_scooter</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 23</td>
    </tr>
    <tr>
      <th>2823</th>
      <td>0x59e9</td>
      <td>PUNERES20DEL01</td>
      <td>22</td>
      <td>5</td>
      <td>18.592718</td>
      <td>73.773572</td>
      <td>18.602718</td>
      <td>73.783572</td>
      <td>28-03-2022</td>
      <td>08:40:00</td>
      <td>08:55:00</td>
      <td>conditions Cloudy</td>
      <td>Low</td>
      <td>2</td>
      <td>Drinks</td>
      <td>scooter</td>
      <td>0</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 17</td>
    </tr>
    <tr>
      <th>3158</th>
      <td>0x1c44</td>
      <td>HYDRES16DEL03</td>
      <td>27</td>
      <td>4.6</td>
      <td>17.440827</td>
      <td>78.393391</td>
      <td>17.500827</td>
      <td>78.453391</td>
      <td>19-03-2022</td>
      <td>21:00:00</td>
      <td>21:05:00</td>
      <td>conditions Sandstorms</td>
      <td>Jam</td>
      <td>1</td>
      <td>Meal</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>No</td>
      <td>Urban</td>
      <td>(min) 23</td>
    </tr>
    <tr>
      <th>93</th>
      <td>0x6d19</td>
      <td>INDORES12DEL02</td>
      <td>38</td>
      <td>4.9</td>
      <td>22.748060</td>
      <td>75.893400</td>
      <td>22.768060</td>
      <td>75.913400</td>
      <td>11-03-2022</td>
      <td>08:40:00</td>
      <td>08:55:00</td>
      <td>conditions Cloudy</td>
      <td>Low</td>
      <td>2</td>
      <td>Drinks</td>
      <td>scooter</td>
      <td>1</td>
      <td>No</td>
      <td>Urban</td>
      <td>(min) 15</td>
    </tr>
    <tr>
      <th>277</th>
      <td>0x4fb8</td>
      <td>VADRES09DEL01</td>
      <td>35</td>
      <td>5</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.070000</td>
      <td>0.070000</td>
      <td>27-03-2022</td>
      <td>17:25:00</td>
      <td>17:35:00</td>
      <td>conditions Fog</td>
      <td>Medium</td>
      <td>0</td>
      <td>Snack</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 37</td>
    </tr>
    <tr>
      <th>459</th>
      <td>0xafd4</td>
      <td>COIMBRES19DEL02</td>
      <td>27</td>
      <td>4.6</td>
      <td>11.022298</td>
      <td>76.998349</td>
      <td>11.042298</td>
      <td>77.018349</td>
      <td>07-03-2022</td>
      <td>11:30:00</td>
      <td>11:40:00</td>
      <td>conditions Sunny</td>
      <td>High</td>
      <td>2</td>
      <td>Buffet</td>
      <td>electric_scooter</td>
      <td>0</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 16</td>
    </tr>
    <tr>
      <th>781</th>
      <td>0xcda0</td>
      <td>ALHRES18DEL02</td>
      <td>31</td>
      <td>4.3</td>
      <td>25.450317</td>
      <td>81.831681</td>
      <td>25.470317</td>
      <td>81.851681</td>
      <td>13-02-2022</td>
      <td>12:00:00</td>
      <td>12:10:00</td>
      <td>conditions Windy</td>
      <td>High</td>
      <td>0</td>
      <td>Buffet</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>Yes</td>
      <td>Metropolitian</td>
      <td>(min) 48</td>
    </tr>
    <tr>
      <th>2113</th>
      <td>0x1255</td>
      <td>VADRES05DEL01</td>
      <td>30</td>
      <td>4.8</td>
      <td>22.310526</td>
      <td>73.170937</td>
      <td>22.380526</td>
      <td>73.240937</td>
      <td>04-03-2022</td>
      <td>00:00:00</td>
      <td>00:15:00</td>
      <td>conditions Stormy</td>
      <td>Low</td>
      <td>0</td>
      <td>Drinks</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 20</td>
    </tr>
    <tr>
      <th>1032</th>
      <td>0xc7e2</td>
      <td>BHPRES18DEL03</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>23.234631</td>
      <td>77.401663</td>
      <td>23.264631</td>
      <td>77.431663</td>
      <td>13-02-2022</td>
      <td>NaN</td>
      <td>18:15:00</td>
      <td>conditions Sandstorms</td>
      <td>Medium</td>
      <td>2</td>
      <td>Snack</td>
      <td>scooter</td>
      <td>0</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 30</td>
    </tr>
    <tr>
      <th>1353</th>
      <td>0x2de8</td>
      <td>COIMBRES14DEL03</td>
      <td>24</td>
      <td>4.9</td>
      <td>11.003681</td>
      <td>76.975525</td>
      <td>11.063681</td>
      <td>77.035525</td>
      <td>07-03-2022</td>
      <td>23:25:00</td>
      <td>23:30:00</td>
      <td>conditions Stormy</td>
      <td>Low</td>
      <td>2</td>
      <td>Drinks</td>
      <td>electric_scooter</td>
      <td>0</td>
      <td>No</td>
      <td>Urban</td>
      <td>(min) 17</td>
    </tr>
    <tr>
      <th>1306</th>
      <td>0x39eb</td>
      <td>VADRES15DEL03</td>
      <td>34</td>
      <td>4.9</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.090000</td>
      <td>0.090000</td>
      <td>06-04-2022</td>
      <td>19:10:00</td>
      <td>19:25:00</td>
      <td>conditions Fog</td>
      <td>Jam</td>
      <td>0</td>
      <td>Drinks</td>
      <td>motorcycle</td>
      <td>1</td>
      <td>Yes</td>
      <td>Metropolitian</td>
      <td>(min) 40</td>
    </tr>
    <tr>
      <th>1723</th>
      <td>0x86cb</td>
      <td>VADRES09DEL03</td>
      <td>25</td>
      <td>4.8</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.030000</td>
      <td>0.030000</td>
      <td>28-03-2022</td>
      <td>23:20:00</td>
      <td>23:35:00</td>
      <td>conditions Sandstorms</td>
      <td>Low</td>
      <td>2</td>
      <td>Buffet</td>
      <td>scooter</td>
      <td>1</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 15</td>
    </tr>
    <tr>
      <th>1379</th>
      <td>0xddb3</td>
      <td>AURGRES16DEL01</td>
      <td>32</td>
      <td>4.8</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.040000</td>
      <td>0.040000</td>
      <td>15-02-2022</td>
      <td>13:15:00</td>
      <td>13:20:00</td>
      <td>conditions Sandstorms</td>
      <td>High</td>
      <td>1</td>
      <td>Drinks</td>
      <td>scooter</td>
      <td>1</td>
      <td>No</td>
      <td>NaN</td>
      <td>(min) 26</td>
    </tr>
    <tr>
      <th>1443</th>
      <td>0x821e</td>
      <td>JAPRES20DEL02</td>
      <td>39</td>
      <td>4</td>
      <td>26.956431</td>
      <td>75.776649</td>
      <td>26.976431</td>
      <td>75.796649</td>
      <td>05-04-2022</td>
      <td>11:20:00</td>
      <td>11:35:00</td>
      <td>conditions Stormy</td>
      <td>High</td>
      <td>2</td>
      <td>Buffet</td>
      <td>scooter</td>
      <td>0</td>
      <td>No</td>
      <td>Metropolitian</td>
      <td>(min) 34</td>
    </tr>
  </tbody>
</table>
</div>



# 4.0 Limpeza & Transansformação

Claramente algumas colunas possuem valores NaN, mas eles não estão aparecendo na checagem de NaNs. Isso pode ser porque eles são do tipo objeto ou estão armazenados como string e possuem algum formato estranho como " NaN", com um espaço em branco.<br>Os primeiros passos serão: remover todos os espaços das colunas com string, convertê-las para o tipo apropriado e remover excesso de NaNs.

## 4.1 Remover espaços & Corrigir tipos de dados e erros de escrita


```python
df_clear = df_raw.copy()
# Remover espaços em branco no início e no final das strings
df_clear = df_clear.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# Converter para tipos númericos onde for necessario
df_clear["Delivery_person_Age"] = df_clear["Delivery_person_Age"].apply(pd.to_numeric, errors="coerce").astype("Int64")
df_clear["Delivery_person_Ratings"] = df_clear["Delivery_person_Ratings"].apply(pd.to_numeric, errors="coerce")
df_clear["multiple_deliveries"] = df_clear["multiple_deliveries"].apply(pd.to_numeric, errors="coerce").astype("Int64")
# Corrigir erro de escrita em colunas
df_clear.rename(columns={"Time_Orderd": "Time_Ordered"}, inplace=True)
# Corrigir erro de escrita em valores
df_clear["City"] = df_clear["City"].str.replace("Metropolitian", "Metropolitan", regex=False)
# Converter para tipo date.time para melhor manipulá-los
df_clear["Order_Date"] = pd.to_datetime(df_clear["Order_Date"], format="%d-%m-%Y").astype("string")
df_clear["Time_Ordered"] = pd.to_datetime(df_clear["Time_Ordered"], format="%H:%M:%S").dt.time.astype("string")
df_clear["Time_Order_picked"] = pd.to_datetime(df_clear["Time_Order_picked"], format="%H:%M:%S").dt.time.astype("string")
# Remover letras da coluna "Time_taken(min)" e conberter tipo para "Int64"
df_clear["Time_taken(min)"] = df_clear["Time_taken(min)"].str.extract(r'(\d+)').astype("Int64")
# Remover excesso de palavras na coluna "Weatherconditions"
df_clear["Weatherconditions"] = df_clear["Weatherconditions"].str.replace("conditions ", "", regex=False)
# Mudar NaNs para "Unknown" em colunas que não guardam valores numéricos
df_clear["Weatherconditions"] = df_clear["Weatherconditions"].str.replace("NaN", "Unknown", regex=False)
df_clear["Road_traffic_density"] = df_clear["Road_traffic_density"].str.replace("NaN", "Unknown", regex=False)
df_clear["City"] = df_clear["City"].str.replace("NaN", "Unknown", regex=False)
df_clear["Festival"] = df_clear["Festival"].str.replace("NaN", "Unknown", regex=False)

```


```python
print(f"Max rating: {df_clear["Delivery_person_Ratings"].max()}\nMin rating: {df_clear["Delivery_person_Ratings"].min()}")
df_clear[df_clear["Delivery_person_Ratings"] > 5.0]
```

    Max rating: 6.0
    Min rating: 1.0
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID</th>
      <th>Delivery_person_ID</th>
      <th>Delivery_person_Age</th>
      <th>Delivery_person_Ratings</th>
      <th>Restaurant_latitude</th>
      <th>Restaurant_longitude</th>
      <th>Delivery_location_latitude</th>
      <th>Delivery_location_longitude</th>
      <th>Order_Date</th>
      <th>Time_Ordered</th>
      <th>Time_Order_picked</th>
      <th>Weatherconditions</th>
      <th>Road_traffic_density</th>
      <th>Vehicle_condition</th>
      <th>Type_of_order</th>
      <th>Type_of_vehicle</th>
      <th>multiple_deliveries</th>
      <th>Festival</th>
      <th>City</th>
      <th>Time_taken(min)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3586</th>
      <td>0x46d</td>
      <td>BANGRES05DEL01</td>
      <td>50</td>
      <td>6.0</td>
      <td>-12.970324</td>
      <td>-77.645748</td>
      <td>13.010324</td>
      <td>77.685748</td>
      <td>2022-03-13</td>
      <td>&lt;NA&gt;</td>
      <td>12:30:00</td>
      <td>Unknown</td>
      <td>Unknown</td>
      <td>3</td>
      <td>Meal</td>
      <td>electric_scooter</td>
      <td>0</td>
      <td>No</td>
      <td>Urban</td>
      <td>25</td>
    </tr>
  </tbody>
</table>
</div>



Há um valor de avaliação de 6,0. Como há apenas um valor "errado" e, assumindo que o máximo é 5 "estrelas", ele será corrigido para 5.


```python
df_clear.loc[df_clear["Delivery_person_Ratings"] > 5.0, "Delivery_person_Ratings"] = 5.0
```

## 4.2 Remover excesso de NaNs


```python
# Para manter a análise simples, linhas com mais de 2 NaNs serão removidas, o que dá ~5% dos dados
df_clear = df_clear.dropna(thresh=len(df_clear.columns) - 2).reset_index(drop=True)
# Há somente 1 NaN em "Time_taken(min)", que será substituído removido pois o trabalho para estipula-lo não é viável
df_clear = df_clear.dropna(subset=["Time_taken(min)"]).reset_index(drop=True)
```


```python
checkData(df_clear)
```

    
    Info dos valores:
    
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4291 entries, 0 to 4290
    Data columns (total 20 columns):
     #   Column                       Non-Null Count  Dtype  
    ---  ------                       --------------  -----  
     0   ID                           4291 non-null   object 
     1   Delivery_person_ID           4291 non-null   object 
     2   Delivery_person_Age          4277 non-null   Int64  
     3   Delivery_person_Ratings      4271 non-null   float64
     4   Restaurant_latitude          4291 non-null   float64
     5   Restaurant_longitude         4291 non-null   float64
     6   Delivery_location_latitude   4291 non-null   float64
     7   Delivery_location_longitude  4291 non-null   float64
     8   Order_Date                   4291 non-null   string 
     9   Time_Ordered                 4287 non-null   string 
     10  Time_Order_picked            4291 non-null   string 
     11  Weatherconditions            4291 non-null   object 
     12  Road_traffic_density         4291 non-null   object 
     13  Vehicle_condition            4291 non-null   int64  
     14  Type_of_order                4291 non-null   object 
     15  Type_of_vehicle              4291 non-null   object 
     16  multiple_deliveries          4189 non-null   Int64  
     17  Festival                     4291 non-null   object 
     18  City                         4291 non-null   object 
     19  Time_taken(min)              4291 non-null   Int64  
    dtypes: Int64(3), float64(5), int64(1), object(8), string(3)
    memory usage: 683.2+ KB
    None
    
    Descrição dos dados:
    
           Delivery_person_Age  Delivery_person_Ratings  Restaurant_latitude  \
    count               4277.0              4271.000000          4291.000000   
    mean             29.449614                 4.630414            17.102314   
    std               5.788815                 0.330637             7.842138   
    min                   15.0                 1.000000           -30.902872   
    25%                   25.0                 4.500000            12.913041   
    50%                   29.0                 4.700000            18.546947   
    75%                   34.0                 4.800000            22.727021   
    max                   50.0                 5.000000            30.914057   
    
           Restaurant_longitude  Delivery_location_latitude  \
    count           4291.000000                 4291.000000   
    mean              70.374837                   17.342799   
    std               21.820543                    7.445809   
    min              -77.645748                    0.010000   
    25%               73.170283                   12.969934   
    50%               75.894377                   18.621440   
    75%               78.024883                   22.781857   
    max               88.433452                   31.035562   
    
           Delivery_location_longitude  Vehicle_condition  multiple_deliveries  \
    count                  4291.000000        4291.000000               4189.0   
    mean                     70.474555           1.000233             0.761996   
    std                      21.703733           0.819204             0.589973   
    min                       0.010000           0.000000                  0.0   
    25%                      73.280610           0.000000                  0.0   
    50%                      75.984377           1.000000                  1.0   
    75%                      78.080363           2.000000                  1.0   
    max                      88.563452           3.000000                  3.0   
    
           Time_taken(min)  
    count           4291.0  
    mean         26.277092  
    std           9.385049  
    min               10.0  
    25%               19.0  
    50%               25.0  
    75%               32.0  
    max               54.0  
    

## 4.3 Unir coordenadas em uma tupla em nova coluna

Para melhor trabalhar com as coordenadas, elas serão armazenadas como uma tupla.



```python
df_clear["Restaurant_location"] = list(zip(df_clear["Restaurant_latitude"], df_clear["Restaurant_longitude"]))
df_clear["Delivery_location"] = list(zip(df_clear["Delivery_location_latitude"], df_clear["Delivery_location_longitude"]))
df_clear.drop(columns=["Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"], inplace=True)
```

## 4.4 Unir datas e horas

Para melhor trabalhar com o tempo, "Order_date" será unido com "Time_Ordered" e "Time_Order_picked". Pelo mesmo motivo, "Time_taken(min)" será transformado em um date.time baseado em "Time_Order_picked" + "Time_taken(min)".


```python
# Une as colunas de data e hora para uma melhor manipulação
df_clear["Time_Ordered"] = pd.to_datetime(df_clear["Order_Date"] + " " + df_clear["Time_Ordered"], format="%Y-%m-%d %H:%M:%S")
df_clear["Time_Order_picked"] = pd.to_datetime(df_clear['Order_Date'] + " " + df_clear["Time_Order_picked"], format="%Y-%m-%d %H:%M:%S")
# Adiciona 1 dia para pedidos feitos antes da meia noite e entregues depois da meia
df_clear["Time_Order_picked"] = df_clear.apply(lambda row: row["Time_Order_picked"] + pd.Timedelta(days=1) if row["Time_Ordered"] > row["Time_Order_picked"] else row["Time_Order_picked"], axis=1)
# Calcula a hora da entrega baseado em Time_order_pick + time_taken
df_clear["Time_Order_delivered"] = df_clear["Time_Order_picked"] + pd.to_timedelta(df_clear["Time_taken(min)"], unit="m")
# Remove as colunas originais de data e tempo
df_clear.drop(["Order_Date", "Time_taken(min)"], axis=1, inplace=True)
```

## 4.5 Preenchendo NaNs


```python
print(f'Mediana de "Delivery_person_Age": {df_clear['Delivery_person_Age'].median()}')
print(f'Média de "Delivery_person_Age": {df_clear['Delivery_person_Age'].mean()}')
```

    Mediana de "Delivery_person_Age": 29.0
    Média de "Delivery_person_Age": 29.449614215571664
    

A coluna "Delivery_person_Age" possui o valor de ~29 tanto para a mediana quanto para a média, então vamos preencher os NaNs com a mediana, pois é um Int e a média é um float.<br>Uma abordagem melhor seria aplicar um método como "KNN", mas neste exercício vamos nos manter no simples.


```python
df_clear["Delivery_person_Age"] = df_clear['Delivery_person_Age'].fillna(df_clear['Delivery_person_Age'].median())
```

"Delivery_person_Ratings" pode ser preenchido com a média baseada no "Delivery_person_ID".


```python
df_aux = df_clear[["Delivery_person_ID", "Delivery_person_Ratings"]].dropna()
df_aux = df_aux.groupby(["Delivery_person_ID"]).mean().reset_index()
df_clear = df_clear.merge(df_aux, on="Delivery_person_ID", how="left", suffixes=('', '_mean'))
df_clear["Delivery_person_Ratings"] = df_clear["Delivery_person_Ratings"].fillna(df_clear["Delivery_person_Ratings_mean"])
df_clear.drop(columns=["Delivery_person_Ratings_mean"], inplace=True)
```

NaNs em "Time_ordered" podem ser preenchidos com base nos outros pedidos, agrupados pelo tipo de pedido.<br>A suposição aqui é que as refeições provavelmente têm um tempo de preparo mais longo do que o buffet, que tem um tempo mais longo do que as bebidas, que têm um tempo mais longo do que as lanches.


```python
df_aux = df_clear[["Time_Ordered", "Time_Order_picked", "Time_Order_delivered", "Type_of_order"]].dropna()
df_aux["Time_to_pick"] = (df_aux["Time_Order_picked"] - df_aux["Time_Ordered"]).dt.total_seconds() / 60
df_aux["Time_to_delivery"] = (df_aux["Time_Order_delivered"] - df_aux["Time_Order_picked"]).dt.total_seconds() / 60
df_aux = df_aux.drop(columns=["Time_Ordered", "Time_Order_picked", "Time_Order_delivered"])
df_times_grouped = df_aux.groupby(["Type_of_order"]).agg(["mean", "median"]).reset_index()
df_times_grouped
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>Type_of_order</th>
      <th colspan="2" halign="left">Time_to_pick</th>
      <th colspan="2" halign="left">Time_to_delivery</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>mean</th>
      <th>median</th>
      <th>mean</th>
      <th>median</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Buffet</td>
      <td>9.781784</td>
      <td>10.0</td>
      <td>26.122391</td>
      <td>25.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Drinks</td>
      <td>9.841954</td>
      <td>10.0</td>
      <td>26.286398</td>
      <td>25.5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Meal</td>
      <td>10.032110</td>
      <td>10.0</td>
      <td>26.225688</td>
      <td>25.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Snack</td>
      <td>9.977252</td>
      <td>10.0</td>
      <td>26.482257</td>
      <td>26.0</td>
    </tr>
  </tbody>
</table>
</div>



A suposição não foi exatamente verdadeira, mas a mediana de "Time_to_pick" pode ser usada para calcular quando os pedidos com NaNs foram feitos sem muita distorção nos dados.


```python
df_clear["Time_Ordered"] = df_clear["Time_Ordered"].fillna(df_clear["Time_Order_picked"] - pd.to_timedelta(df_times_grouped.loc[0, ("Time_to_pick", "median")], unit="m"))
```

Em "multiple_delivery", a suposição é: se não é uma entrega múltipla, essa entrada não foi preenchida, então os NaNs serão preenchidos com 1.


```python
df_clear["multiple_deliveries"] = df_clear["multiple_deliveries"].fillna(1)
```


```python
checkData(df_clear)
```

    
    Info dos valores:
    
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4291 entries, 0 to 4290
    Data columns (total 17 columns):
     #   Column                   Non-Null Count  Dtype         
    ---  ------                   --------------  -----         
     0   ID                       4291 non-null   object        
     1   Delivery_person_ID       4291 non-null   object        
     2   Delivery_person_Age      4291 non-null   Int64         
     3   Delivery_person_Ratings  4291 non-null   float64       
     4   Time_Ordered             4291 non-null   datetime64[ns]
     5   Time_Order_picked        4291 non-null   datetime64[ns]
     6   Weatherconditions        4291 non-null   object        
     7   Road_traffic_density     4291 non-null   object        
     8   Vehicle_condition        4291 non-null   int64         
     9   Type_of_order            4291 non-null   object        
     10  Type_of_vehicle          4291 non-null   object        
     11  multiple_deliveries      4291 non-null   Int64         
     12  Festival                 4291 non-null   object        
     13  City                     4291 non-null   object        
     14  Restaurant_location      4291 non-null   object        
     15  Delivery_location        4291 non-null   object        
     16  Time_Order_delivered     4291 non-null   datetime64[ns]
    dtypes: Int64(2), datetime64[ns](3), float64(1), int64(1), object(10)
    memory usage: 578.4+ KB
    None
    
    Descrição dos dados:
    
           Delivery_person_Age  Delivery_person_Ratings  \
    count               4291.0              4291.000000   
    mean             29.448147                 4.630762   
    min                   15.0                 1.000000   
    25%                   25.0                 4.500000   
    50%                   29.0                 4.700000   
    75%                   34.0                 4.800000   
    max                   50.0                 5.000000   
    std               5.779419                 0.329956   
    
                            Time_Ordered              Time_Order_picked  \
    count                           4291                           4291   
    mean   2022-03-14 13:26:58.503845120  2022-03-14 13:36:53.120484864   
    min              2022-02-11 00:00:00            2022-02-11 00:10:00   
    25%              2022-03-05 09:57:30            2022-03-05 10:10:00   
    50%              2022-03-15 17:50:00            2022-03-15 18:00:00   
    75%              2022-03-27 19:35:00            2022-03-27 19:45:00   
    max              2022-04-06 23:55:00            2022-04-07 00:05:00   
    std                              NaN                            NaN   
    
           Vehicle_condition  multiple_deliveries           Time_Order_delivered  
    count        4291.000000               4291.0                           4291  
    mean            1.000233             0.767653  2022-03-14 14:03:09.745979904  
    min             0.000000                  0.0            2022-02-11 00:27:00  
    25%             0.000000                  0.0            2022-03-05 10:32:30  
    50%             1.000000                  1.0            2022-03-15 18:38:00  
    75%             2.000000                  1.0            2022-03-27 20:14:00  
    max             3.000000                  3.0            2022-04-07 00:48:00  
    std             0.819204             0.584044                            NaN  
    

# 5.0 Análise descritiva

## 5.1 Primeiras KBQs
Por enquanto, as perguntas de négocio serão respondidas sem o uso de técnicas intermediárias/avançadas como groupby, agg, plotting, machine learning, etc...

### 1. Qual o número total de entregas cadastradas na base de dados?
**Resposta:** O número total de entregas cadastrados na base de dados é 4291.


```python
len(df_clear)
```




    4291



### 2. Quantos entregadores únicos existem na base de dados?
**Resposta:** Há 1131 IDs únicos na base de dados, porem aparentemente não são entregadores, mas sim empresas que oferecem o serviço de entrega, pois há multiplas idades para o mesmo ID de entregador.

Primeiramente foi notado nos datasets abaixo que há multiplas idades para o mesmo ID de entregador, o que sugere que provavelmente o ID não é do entregador, mas provavelmente da empresa que oferece o serviço de entrega.
Note que, apesar de não ser usado técnicas como groupby e agg, foi aberto uma exceção para o código abaixo, pois ele não visa responder a pergunta, mas sim apontar uma inconsistência na base de dados.


```python
df_aux = df_clear[["Delivery_person_ID", "Delivery_person_Age"]].dropna()
df_age_grouped = df_aux.groupby(["Delivery_person_ID"]).agg(["count"]).reset_index()
df_age_grouped
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>Delivery_person_ID</th>
      <th>Delivery_person_Age</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AGRRES010DEL01</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AGRRES010DEL02</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AGRRES01DEL02</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AGRRES01DEL03</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AGRRES02DEL02</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1126</th>
      <td>VADRES19DEL02</td>
      <td>7</td>
    </tr>
    <tr>
      <th>1127</th>
      <td>VADRES19DEL03</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1128</th>
      <td>VADRES20DEL01</td>
      <td>5</td>
    </tr>
    <tr>
      <th>1129</th>
      <td>VADRES20DEL02</td>
      <td>7</td>
    </tr>
    <tr>
      <th>1130</th>
      <td>VADRES20DEL03</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>1131 rows × 2 columns</p>
</div>




```python
df_clear.loc[df_clear['Delivery_person_ID'] == 'VADRES19DEL02', ["Delivery_person_ID", "Delivery_person_Age"]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Delivery_person_ID</th>
      <th>Delivery_person_Age</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>921</th>
      <td>VADRES19DEL02</td>
      <td>38</td>
    </tr>
    <tr>
      <th>2160</th>
      <td>VADRES19DEL02</td>
      <td>33</td>
    </tr>
    <tr>
      <th>2972</th>
      <td>VADRES19DEL02</td>
      <td>34</td>
    </tr>
    <tr>
      <th>3091</th>
      <td>VADRES19DEL02</td>
      <td>28</td>
    </tr>
    <tr>
      <th>3326</th>
      <td>VADRES19DEL02</td>
      <td>36</td>
    </tr>
    <tr>
      <th>3390</th>
      <td>VADRES19DEL02</td>
      <td>28</td>
    </tr>
    <tr>
      <th>4205</th>
      <td>VADRES19DEL02</td>
      <td>38</td>
    </tr>
  </tbody>
</table>
</div>



Portanto será tratado como "ID único" e não "entregador único".


```python
# Get the size of the unique values in the column Delivery_person_ID
len(df_clear["Delivery_person_ID"].unique())
```




    1131



### 3. Qual a idade do entregador mais velho? E do mais novo?
**Resposta:** A maior idadeade é 50 anos e a menor idade é 15 anos.


```python
df_clear["Delivery_person_Age"].sort_values(ascending=True)
```




    2292    15
    2787    15
    2833    15
    1944    20
    3031    20
            ..
    65      39
    2976    39
    3029    39
    4277    39
    3448    50
    Name: Delivery_person_Age, Length: 4291, dtype: Int64



### 4. Qual o ID do entregador com a maior idade? E o ID do entregador com a menor idade?
**Resposta:** O ID do entregador mais velho é "BANGRES05DEL01" e o ID do entregador mais novo é "JAPRES15DEL03".


```python
max_age_row = df_clear.loc[df_clear["Delivery_person_Age"].idxmax()]
min_age_row = df_clear.loc[df_clear["Delivery_person_Age"].idxmin()]
age_max_min = {
    "max": {
        "Delivery_person_ID": str(max_age_row["Delivery_person_ID"]),
        "Delivery_person_Age": int(max_age_row["Delivery_person_Age"])
    },
    "min": {
        "Delivery_person_ID": str(min_age_row["Delivery_person_ID"]),
        "Delivery_person_Age": int(min_age_row["Delivery_person_Age"])
    }
}
age_max_min

```




    {'max': {'Delivery_person_ID': 'BANGRES05DEL01', 'Delivery_person_Age': 50},
     'min': {'Delivery_person_ID': 'JAPRES15DEL03', 'Delivery_person_Age': 15}}



### 5. Quais os nomes das condições climáticas?
**Resposta:** As condições climáticas são: 
- "Sunny"
- "Stormy"
- "Sandstorms"
- "Cloudy"
- "Fog"
- "Windy"
- "Unknown".

Lembrando que "Unknown" foi criado para conter os valores nulos da coluna.


```python
df_clear["Weatherconditions"].unique()
```




    array(['Sunny', 'Stormy', 'Sandstorms', 'Cloudy', 'Fog', 'Windy',
           'Unknown'], dtype=object)



### 6. Quantas entregas foram realizadas sob condições climáticas de tempestade de areia (Sandstorms)?
**Resposta:** Foram feitas 697 entregas com a condição "Sandstorms".


```python
len(df_clear.loc[df_clear["Weatherconditions"] == "Sandstorms", "Weatherconditions"])
```




    697



### 7. Quais eram as condicões climáticas da data mais recente de entrega?
**Resposta:** A condição climática da data mais recente de entrega foi "Fog" (Neblina).


```python
df_clear.loc[df_clear["Time_Order_delivered"] == df_clear["Time_Order_delivered"].max(), "Weatherconditions"]
```




    1288    Fog
    Name: Weatherconditions, dtype: object



### 8. Quantos tipos de densidade de trânsito existem na base de dados? Quais os nomes delas?
**Resposta:** Existem 5 tipos de densidade de trânsito na base de dados:
- High
- Jam
- Low
- Medium
- Unknown

Lembrando que "Unknown" foi criado para conter os valores nulos da coluna.


```python
print(f"{len(df_clear["Road_traffic_density"].unique())} tipos de densidade.\n{df_clear["Road_traffic_density"].unique()}.")
```

    5 tipos de densidade.
    ['High' 'Jam' 'Low' 'Medium' 'Unknown'].
    

### 9. Quantas entregas foram feitas em cada condição climática?
**Resposta:** A quantidade de entregas feitas em cada condição climática é: 
1. Fog: 758
2. Windy: 725
3. Cloudy: 707
4. Stormy: 704
5. Sandstorms: 697
6. Sunny: 696
7. Unknown: 4


```python
for condition in df_clear["Weatherconditions"].unique():
    print(f"{condition}: {len(df_clear.loc[df_clear["Weatherconditions"] == condition, "Weatherconditions"])}")
```

    Sunny: 696
    Stormy: 704
    Sandstorms: 697
    Cloudy: 707
    Fog: 758
    Windy: 725
    Unknown: 4
    

### 10. Quantos entregadores únicos fizeram entregas em cada condição climática?
**Resposta:** A quantidade de entregadores únicos que fizeram entregas em cada condição climática é: 
1. Sunny: 529
2. Windy: 523
3. Cloudy: 520
4. Fog: 511
5. Stormy: 504
6. Sandstorms: 504
7. Unknown: 4


```python
for condition in df_clear["Weatherconditions"].unique():
    print(f"{condition}: {df_clear.loc[df_clear["Weatherconditions"] == condition, "Delivery_person_ID"].nunique()}")
```

    Sunny: 529
    Stormy: 504
    Sandstorms: 504
    Cloudy: 520
    Fog: 511
    Windy: 523
    Unknown: 4
    

### 11. Quantas entregas foram feitas em cada tipo de densidade de trânsito?
**Resposta:** A quantidade de entregas feitas em cada condição de transito é: 
1. Low: 1504
2. Jam: 1303
3. Medium: 1059
4. High: 421
5. Unknown: 4


```python
for condition in df_clear["Road_traffic_density"].unique():
    print(f"{condition}: {len(df_clear.loc[df_clear["Road_traffic_density"] == condition, "Road_traffic_density"])}")
```

    High: 421
    Jam: 1303
    Low: 1504
    Medium: 1059
    Unknown: 4
    

### 12. Quantos entregadores únicos fizeram entregas em cada tipo de densidade de trânsito?
**Resposta:** A quantidade de entregadores únicos que fizeram entregas em cada densidade de trânsito é: 
1. Low: 784
2. Jam: 740
3. Medium: 649
4. High: 293
5. Unknown: 4


```python
for condition in df_clear["Road_traffic_density"].unique():
    print(f"{condition}: {df_clear.loc[df_clear["Road_traffic_density"] == condition, "Delivery_person_ID"].nunique()}")
```

    High: 293
    Jam: 740
    Low: 784
    Medium: 649
    Unknown: 4
    

### 13. Quantos tipos de cidades únicas existem na base? Quais são os seus nomes?
***Resposta:*** Há 4 tipos de cidades únicas na base e seus nomes são: 
- Urban
- Metropolitian
- Semi-Urban
- Unknown


```python
print(f"Há {len(df_clear["City"].unique())} tipos de cidades únicas na base e seus nomes são: {df_clear["City"].unique()}.")
```

    Há 4 tipos de cidades únicas na base e seus nomes são: ['Urban' 'Metropolitan' 'Semi-Urban' 'Unknown'].
    

### 14. Quantos tipos de veículos únicos existem na base? Quais são seus nomes?
***Resposta:*** Há 4 tipos de veículos únicos na base e seus nomes são:
- Bicycle
- scooter
- motorcycle
- electric_scooter


```python
print(f"Há {len(df_clear["Type_of_vehicle"].unique())} tipos de veículos únicos na base e seus nomes são: {df_clear["Type_of_vehicle"].unique()}.")
```

    Há 4 tipos de veículos únicos na base e seus nomes são: ['motorcycle' 'scooter' 'electric_scooter' 'bicycle'].
    

### 15. Qual o tipo de veículo que mais vez entregas com a condição de trânsito pesado (High)?
***Resposta:*** O tipo de veículo que mais fez entregas com a condição de trânsito pesado foi motorcycle, com 250 entregas.


```python
df_clear.loc[df_clear["Road_traffic_density"] == "High", "Type_of_vehicle"].value_counts()
```




    Type_of_vehicle
    motorcycle          250
    scooter             140
    electric_scooter     31
    Name: count, dtype: int64



### 16. Qual o tipo de pedido mais feito durante condições climáticas de tempestade de areia?
***Resposta:*** O tipo de pedido mas feito durante a condição climáticas de tempestade de areia foi meal, com 193 entregas.


```python
df_clear.loc[df_clear["Weatherconditions"] == "Sandstorms", "Type_of_order"].value_counts()
```




    Type_of_order
    Meal      193
    Snack     182
    Buffet    161
    Drinks    161
    Name: count, dtype: int64



### 17. Qual o tipo de cidade com o maior número de pedidos de Bebidas (Drinks) feito em Scooter?
***Resposta:*** O tipo de cidade com o maior número de pedidos de bebidas feito em scooter foi Metropolitan, com 260 pedidos.


```python
df_clear.loc[(df_clear["Type_of_order"] == "Drinks") & (df_clear["Type_of_vehicle"] == "scooter"), "City"].value_counts()
```




    City
    Metropolitan    260
    Urban            75
    Unknown          15
    Name: count, dtype: int64



### 18. Qual o tipo de cidade com o (os) entregador mais velho? E o nome da cidade com o (os) entregadores mais novos?
***Resposta:*** O tipo de cidade com o entregador mais velho é Urban e o tipo de cidade com 2 dos 3 entregadores mais novos é Metropolitan.


```python
df_clear.loc[df_clear["Delivery_person_Age"] == df_clear["Delivery_person_Age"].max(), "City"]
```




    3448    Urban
    Name: City, dtype: object



Há um unico entregador mais velho, que está no tipo de cidade Urban.


```python
df_clear.loc[df_clear["Delivery_person_Age"] == df_clear["Delivery_person_Age"].min(), "City"]
```




    2292           Urban
    2787    Metropolitan
    2833    Metropolitan
    Name: City, dtype: object



Há 3 entregadores mais novos, onde 2 estão no tipo de cidade Metropolitan.

### 19. Quantas entregas foram feitas durante o Festival?
***Resposta:*** Foram feitas 91 entregas durante o Festival.


```python
len(df_clear.loc[df_clear["Festival"] == "Yes", "ID"])
```




    91



### 20. Quantos tipos de cidades únicas tiveram entregas feitas durante o Festival?
***Resposta:*** Houve 4 tipos de cidades únicas que tiveram entregas feitas durante o Festival.


```python
df_clear.loc[df_clear["Festival"] == "Yes", "City"].nunique()
```




    4



### 21. Quantas entregas foram feitas durante o Festival no tipo de cidade Urban?
***Resposta:*** Foram feitas 18 entregas durante o Festival no tipo de cidade Urban.


```python
df_clear.loc[(df_clear["Festival"] == "Yes") & (df_clear["City"] == "Urban"), "ID"].count()
```




    np.int64(18)



## 5.2 Próximas KBQs
As próximas perguntas de negócio serão respondidas usando o método SAPE e o uso de tecnicas intermediarias como groupby e agg.

### 1. Qual a média e mediana de idade dos entregadores por tipo de cidade?
**Resposta:** A média e mediana de idade dos entregadores por tipo de cidade é:
- Metropolitian: Média: 29.68, Mediana: 30
- Urban: Média: 28.66, Mediana: 28
- Semi-Urban: Média: 34.33, Mediana: 36
- Unknown: Média: 28.72, Mediana: 28.0


```python
# SAída: DataFrame com a média e mediana de idade dos entregadores agrupado por tipo de cidade
# Processo: Agrupar os dados por tipo de cidade e calcular a média e mediana da idade dos entregadores
# Entrada: DataFrame com os dados limpos
df_clear.groupby("City").agg({"Delivery_person_Age": ["mean", "median"]})
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="2" halign="left">Delivery_person_Age</th>
    </tr>
    <tr>
      <th></th>
      <th>mean</th>
      <th>median</th>
    </tr>
    <tr>
      <th>City</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Metropolitan</th>
      <td>29.685919</td>
      <td>30.0</td>
    </tr>
    <tr>
      <th>Semi-Urban</th>
      <td>34.333333</td>
      <td>36.0</td>
    </tr>
    <tr>
      <th>Unknown</th>
      <td>28.722222</td>
      <td>28.0</td>
    </tr>
    <tr>
      <th>Urban</th>
      <td>28.663147</td>
      <td>28.0</td>
    </tr>
  </tbody>
</table>
</div>



### 2. Qual a média das avaliações das entregas feitas por densidade de tráfego?
**Resposta:** A média das avaliações das entregas feitas por densidade de tráfego é:
- Low: 4.63
- Medium: 4.65
- High: 4.67
- Jam: 4.60
- Unknown: 2.00


```python
# SAída: DataFrame com a média das avaliações das entregas feitas agrupadas por densidade de tráfego
# Processo: Agrupar os dados por densidade de tráfego e calcular a média das avaliações das entregas
# Entrada: DataFrame com os dados limpos
df_clear.groupby("Road_traffic_density").agg({"Delivery_person_Ratings": "mean"})
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Delivery_person_Ratings</th>
    </tr>
    <tr>
      <th>Road_traffic_density</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>High</th>
      <td>4.674525</td>
    </tr>
    <tr>
      <th>Jam</th>
      <td>4.601318</td>
    </tr>
    <tr>
      <th>Low</th>
      <td>4.635853</td>
    </tr>
    <tr>
      <th>Medium</th>
      <td>4.652297</td>
    </tr>
    <tr>
      <th>Unknown</th>
      <td>2.000000</td>
    </tr>
  </tbody>
</table>
</div>



### 3. Qual a média, mediana e desvio padrão das entregas feitas agrupadas por tipo de cidade e tipo de veículo?
**Resposta:** Agrupados por tipo de cidade e tipo de veículo, a média, mediana e desvio padrão das entregas feitas é:
- Metropolitan
    - Bicyle: média 20.00, mediana 20.00, desvio padrão NaN
    - Electric Scooter: média 25.51, mediana 26.00, desvio padrão 8.39
    - Motorcycle: média 28.41, mediana 27.00, desvio padrão 9.35
    - Scooter: média 25.51, mediana 25.00, desvio padrão 8.62
- Urban
    - Scooter: média 21.33, mediana 19.50, desvio padrão 7.85
    - Electric Scooter: média 20.82, mediana 19.00, desvio padrão 7.65
    - Motorcycle: média 24.06, mediana 23.00, desvio padrão 9.58
- Semi-Urban
    - Scooter: média 49.00, mediana 49.00, desvio padrão NaN
    - Motorcycle: média 50.21, mediana 50.00, desvio padrão 2.60
- Unknown
    - Electric Scooter: média 20.82, mediana 19.00, desvio padrão 7.65
    - Mortorcycle: média 24.46, mediana 23.00, desvio padrão 9.58
    - Scooter: média 21.33, mediana 19.50, desvio padrão 7.85

*OBS:*<br>
&nbsp;&nbsp;&nbsp;&nbsp; - *Valores representam minutos, por exemplo, 1.5 representa 1 minuto e 30 segundos.*<br>
&nbsp;&nbsp;&nbsp;&nbsp; - *Valores NaN indicam que não há variação, ou seja, só há um valor para aquele grupo.*


```python
# SAída: DataFrame com a média, mediana e desvio padrão das entregas feitas agrupadas por tipo de cidade e tipo de veículo
# Processo: Agrupar as entregas por tipo de cidade e tipo de veículo e calcular a média, mediana e desvio padrão
# Entrada: DataFrame com os dados limpos
df = df_clear[["City", "Type_of_vehicle"]].copy()
df["time_diff(min)"] = (df_clear["Time_Order_delivered"] - df_clear["Time_Order_picked"]).dt.total_seconds() / 60
df.groupby(["City", "Type_of_vehicle"]).agg({"time_diff(min)": ["mean", "median", "std"]})

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th colspan="3" halign="left">time_diff(min)</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th>mean</th>
      <th>median</th>
      <th>std</th>
    </tr>
    <tr>
      <th>City</th>
      <th>Type_of_vehicle</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="4" valign="top">Metropolitan</th>
      <th>bicycle</th>
      <td>20.000000</td>
      <td>20.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>electric_scooter</th>
      <td>25.518987</td>
      <td>26.0</td>
      <td>8.396722</td>
    </tr>
    <tr>
      <th>motorcycle</th>
      <td>28.413066</td>
      <td>27.0</td>
      <td>9.350148</td>
    </tr>
    <tr>
      <th>scooter</th>
      <td>25.519099</td>
      <td>25.0</td>
      <td>8.624229</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">Semi-Urban</th>
      <th>motorcycle</th>
      <td>50.214286</td>
      <td>50.0</td>
      <td>2.607049</td>
    </tr>
    <tr>
      <th>scooter</th>
      <td>49.000000</td>
      <td>49.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">Unknown</th>
      <th>electric_scooter</th>
      <td>14.818182</td>
      <td>15.0</td>
      <td>2.891995</td>
    </tr>
    <tr>
      <th>motorcycle</th>
      <td>24.067797</td>
      <td>24.0</td>
      <td>8.571936</td>
    </tr>
    <tr>
      <th>scooter</th>
      <td>22.750000</td>
      <td>21.5</td>
      <td>8.739149</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">Urban</th>
      <th>electric_scooter</th>
      <td>20.827586</td>
      <td>19.0</td>
      <td>7.658719</td>
    </tr>
    <tr>
      <th>motorcycle</th>
      <td>24.467308</td>
      <td>23.0</td>
      <td>9.585378</td>
    </tr>
    <tr>
      <th>scooter</th>
      <td>21.332353</td>
      <td>19.5</td>
      <td>7.856652</td>
    </tr>
  </tbody>
</table>
</div>



### 4. Qual a primeira e a última data de entrega por cada tipo de cidade?
**Resposta:** A primeira e última data de entrega por cada tipo de cidade são as seguintes:	
- Metropolitan: primeira em *2022-02-11 08:49:00*, e última em *2022-04-07 00:40:00*
- Semi-Urban: primeira em *2022-02-12 20:25:00*, e última em *2022-04-04 22:19:00*
- Unknown: primeira em *2022-02-11 23:55:00*, e última em	*2022-04-07 00:48:00*
- Urban: primeira em *2022-02-11 00:27:00*, e última em *2022-04-07 00:22:00*


```python
# SAída: DataFrame com a primeira e a última data de entrega por cada tipo de cidade
# Processo: Agrupar as entregas por tipo de cidade e recuperar a primeira e a última data de entrega
# Entrada: DataFrame com os dados limpos
df_clear.groupby("City")["Time_Order_delivered"].agg(["min", "max"])
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>min</th>
      <th>max</th>
    </tr>
    <tr>
      <th>City</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Metropolitan</th>
      <td>2022-02-11 08:49:00</td>
      <td>2022-04-07 00:40:00</td>
    </tr>
    <tr>
      <th>Semi-Urban</th>
      <td>2022-02-12 20:25:00</td>
      <td>2022-04-04 22:19:00</td>
    </tr>
    <tr>
      <th>Unknown</th>
      <td>2022-02-11 23:55:00</td>
      <td>2022-04-07 00:48:00</td>
    </tr>
    <tr>
      <th>Urban</th>
      <td>2022-02-11 00:27:00</td>
      <td>2022-04-07 00:22:00</td>
    </tr>
  </tbody>
</table>
</div>



### 5. Qual a média de avaliações das entregas feitas por condições climáticas?
**Resposta:** A média de avaliações das entregas feitas agrupadas por condições climáticas é:
1. Fog:           4.65
2. Sunny:         4.64
3. Sandstorms:    4.63
4. Cloudy:        4.62
5. Windy:         4.62
6. Stormy:        4.61
7. Unknown:       2.00


```python
# SAída: Média de avaliações das entregas feitas por condições climáticas
# Processo: Agrupar as entregas por condições climáticas e calcular a média das avaliações
# Entrada: DataFrame com os dados limpos
df_clear.groupby("Weatherconditions")["Delivery_person_Ratings"].mean()
```




    Weatherconditions
    Cloudy        4.624656
    Fog           4.652101
    Sandstorms    4.633193
    Stormy        4.614725
    Sunny         4.648521
    Unknown       2.000000
    Windy         4.625103
    Name: Delivery_person_Ratings, dtype: float64



### 6. Qual o valor da avaliação mais baixa feita por tipo de condição climática e densidade de tráfego?
**Resposta:** Os valores das avaliações mais baixas feitas agrupadas por tipo de condição climática e densidade de tráfego são as seguintes:
- Cloudy: 
    - High: 4.0
    - Jam: 4.0
    - Low: 3.5
    - Medium: 4.0
- Fog:
    - High: 4.0
    - Jam: 4.0
    - Low: 3.5
    - Medium: 4.0
- Sandstorms:
    - High: 4.0
    - Jam: 3.5
    - Low: 4.0
    - Medium: 3.5
- Stormy:
    - High: 4.0
    - Jam: 3.5
    - Low: 4.0
    - Medium: 3.5
- Sunny:
    - High: 3.5
    - Jam: 3.5
    - Low: 2.5
    - Medium: 4.0
- Windy:
    - High: 4.0
    - Jam: 3.5
    - Low: 4.0
    - Medium: 3.5
- Unknown:
    - Unknown: 1.0


```python
# SAída: Valor da avaliação mais baixa agrupada por tipo de condição climática e densidade de tráfego
# Processo: Agrupar as entregas por tipo de condição climática e densidade de tráfego e calcular o valor mínimo das avaliações
# Entrada: DataFrame com os dados limpos
df_clear.groupby(["Weatherconditions", "Road_traffic_density"])["Delivery_person_Ratings"].agg(["min"])
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>min</th>
    </tr>
    <tr>
      <th>Weatherconditions</th>
      <th>Road_traffic_density</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="4" valign="top">Cloudy</th>
      <th>High</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Jam</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Low</th>
      <td>3.5</td>
    </tr>
    <tr>
      <th>Medium</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Fog</th>
      <th>High</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Jam</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Low</th>
      <td>3.5</td>
    </tr>
    <tr>
      <th>Medium</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Sandstorms</th>
      <th>High</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Jam</th>
      <td>3.5</td>
    </tr>
    <tr>
      <th>Low</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Medium</th>
      <td>3.5</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Stormy</th>
      <th>High</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Jam</th>
      <td>3.5</td>
    </tr>
    <tr>
      <th>Low</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Medium</th>
      <td>3.5</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Sunny</th>
      <th>High</th>
      <td>3.5</td>
    </tr>
    <tr>
      <th>Jam</th>
      <td>3.5</td>
    </tr>
    <tr>
      <th>Low</th>
      <td>2.5</td>
    </tr>
    <tr>
      <th>Medium</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Unknown</th>
      <th>Unknown</th>
      <td>1.0</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Windy</th>
      <th>High</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Jam</th>
      <td>3.5</td>
    </tr>
    <tr>
      <th>Low</th>
      <td>4.0</td>
    </tr>
    <tr>
      <th>Medium</th>
      <td>3.5</td>
    </tr>
  </tbody>
</table>
</div>



### 7. Qual a média, mediana e desvio padrão das avaliações por cada tipo de condições de veículos?
**Resposta:** A média, mediana e desvio padrão das avaliações por cada tipo de condições de veículos são as seguintes:
- 0:
    - média: 4.60
    - mediana: 4.7
    - desvio padrão: 0.29
- 1:
    - média: 4.63
    - mediana: 4.7
    - desvio padrão: 0.35
- 2:
    - média: 4.65
    - mediana: 4.7
    - desvio padrão: 0.29
- 3:
    - média: 2.00
    - mediana:	1.00
    - desvio padrão:	2.00


```python
# SAída: DataFrame com a média, mediana e desvio padrão das avaliações por cada tipo de condições de veículos
# Processo: Agrupar as entregas por tipo de condições de veículos e calcular a média, mediana e desvio padrão das avaliações
# Entrada: DataFrame com os dados limpos
df_clear.groupby("Vehicle_condition")["Delivery_person_Ratings"].agg(["mean", "median", "std"])
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>mean</th>
      <th>median</th>
      <th>std</th>
    </tr>
    <tr>
      <th>Vehicle_condition</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4.609922</td>
      <td>4.7</td>
      <td>0.293908</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4.631220</td>
      <td>4.7</td>
      <td>0.353454</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4.658615</td>
      <td>4.7</td>
      <td>0.294774</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2.000000</td>
      <td>1.0</td>
      <td>2.000000</td>
    </tr>
  </tbody>
</table>
</div>



### 8. Qual a avaliação média das entregas feitas durante o Festival?
**Resposta:** A média das das avaliações das entregas feitas durante o Festival é 4.46.


```python
# SAída: Avaliação média das entregas feitas durante o Festival
# Processo: Filtrar as entregas feitas durante o Festival e calcular a média das avaliações
# Entrada: DataFrame com os dados limpos
df_clear[df_clear["Festival"] == "Yes"]["Delivery_person_Ratings"].mean()
```




    np.float64(4.461538461538461)



### 9. Qual a menor avaliação feita em uma entrega durante o Festival por cidade?
**Resposta:** As menores avaliações feitas em uma entrega durante o Festival agrupada por cidade são as seguintes:
- Metropolitan: 2.5
- Semi-Urban: 3.5
- Urban: 3.5
- Unknown: 4.6


```python
# SAída: Menor avaliação feita em uma entrega durante o Festival por cidade
# Processo: Filtrar as entregas feitas durante o Festival e agrupar por cidade para encontrar a menor avaliação
# Entrada: DataFrame com os dados limpos
df_clear[df_clear["Festival"] == "Yes"].groupby("City")["Delivery_person_Ratings"].min()
```




    City
    Metropolitan    2.5
    Semi-Urban      3.5
    Unknown         4.6
    Urban           3.5
    Name: Delivery_person_Ratings, dtype: float64



### 10. Qual a maior avaliação feita por tipo de pedido?
**Resposta:** As maiores avaliações agrupadas por tipo de pedido são:
- Buffet: 5.0
- Drinks: 5.0
- Meal: 5.0
- Snack: 5.0


```python
# SAída: Maior avaliação feita por tipo de pedido
# Processo: Agrupar por tipo de pedido e encontrar a maior avaliação
# Entrada: DataFrame com os dados limpos
df_clear.groupby("Type_of_order")["Delivery_person_Ratings"].max()
```




    Type_of_order
    Buffet    5.0
    Drinks    5.0
    Meal      5.0
    Snack     5.0
    Name: Delivery_person_Ratings, dtype: float64



# 6.0 Converter notebook para Markdown


```python
# Carregar o notebook
notebook_filename = "notebook.ipynb"
with open(notebook_filename, 'r', encoding='utf-8') as f:
    notebook_content = read(f, as_version=4)
# Converter para Markdown
exporter = MarkdownExporter()
markdown_content, resources = exporter.from_notebook_node(notebook_content)
markdown_filename = os.path.splitext(notebook_filename)[0] + ".md"
with open(markdown_filename, 'w', encoding='utf-8') as f:
    f.write(markdown_content)
# Salvar recursos adicionais, se existirem
if 'outputs' in resources:
    output_dir = os.path.splitext(notebook_filename)[0] + "_files"
    os.makedirs(output_dir, exist_ok=True)
    for resource_name, resource_data in resources['outputs'].items():
        with open(os.path.join(output_dir, resource_name), 'wb') as f:
            f.write(resource_data)
```
