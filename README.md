This is an exercise in learning how to use Keras/TensorFlow.

I really don't know what I'm doing.  I'm mostly blindly following the
examples in the documentation without knowing what most of the
terminology is or what most of the parameters mean.

First set of predictions for 2019 week 9 (the Washington-Buffalo and
Minnesota-KC inputs for model2 must somehow be way out of the range of
the training data.  Once again, model2 thinks San Francisco is due to
lose.  model2 also likes Houston, Tennessee, and Seattle):
model1              | model2                    | actual
------------------- | ------------------------- | ------
SFO 25 crd 23 12.0% | sfo 20 CRD 39 99.0%       |
HTX 26 jax 26 7.0%  | HTX 33 jax 14 1.0%        |
OTI 19 car 24 9.0%  | OTI 35 car 23 1.0%        |
was 17 BUF 24 70.0% | was 140 BUF 155 83.0% :x: |
clt 18 PIT 23 67.0% | clt 29 pit 24 54.0%       |
chi 18 phi 23 58.0% | CHI 13 phi 17 7.0%        |
nyj 19 MIA 24 66.0% | NYJ 29 mia 20 17.0%       |
MIN 28 kan 21 35.0% | min 181 KAN 188 86.0% :x: |
tam 23 SEA 27 69.0% | tam 31 SEA 41 99.0%       |
DET 23 rai 27 39.0% | det 24 rai 37 55.0%       |
CLE 20 den 25 9.0%  | cle 18 DEN 20 87.0%       |
GNB 26 sdg 20 38.0% | GNB 24 sdg 26 31.0%       |
nwe 24 rav 24 55.0% | nwe 24 RAV 37 93.0%       |
dal 25 NYG 19 60.0% | DAL 26 nyg 28 10.0%       |

First set of predictions for 2019 week 8 (model1 tends to pick San
Francisco over Carolina, while model2 consistently picks Carolina over
San Francisco.  For the Thursday game, model2 consistently projects
Minnesota to score around 40 and to win by around 20 over Washington.
model1 and model2 also like Seattle and New Orleans):

model1                                     | model2                                      | actual
------------------------------------------ | ------------------------------------------- | ------
was   16 MIN   29 98.0% :heavy_check_mark: | was   21 MIN   41 100.0% :heavy_check_mark: | 9-19
sdg   21 chi   24 55.0% :x:                | SDG   23 chi   27 15.0%                     | 17-16
phi   18 buf   24 40.0% :x:                | phi   11 BUF   20 77.0% :x:                 | 31-13
sea   27 atl   20 56.0%                    | SEA   39 atl   14 0.0% :heavy_check_mark:   | 27-20
cin   19 RAM   25 63.0% :heavy_check_mark: | CIN   23 ram   19 26.0% :x:                 | 10-24
TAM   23 oti   23 32.0%                    | TAM   20 oti   21 7.0%                      | 23-27
crd   18 NOR   25 83.0% :heavy_check_mark: | crd   14 NOR   23 100.0% :heavy_check_mark: | 9-31
nyj   17 JAX   27 100.0% :heavy_check_mark:| nyj   15 JAX   32 65.0% :heavy_check_mark:  | 15-29
rai   21 HTX   28 65.0% :heavy_check_mark: | RAI   22 htx   22 32.0% :x:                 | 24-27
nyg   19 DET   23 75.0% :heavy_check_mark: | nyg   18 DET   19 95.0% :heavy_check_mark:  | 26-31
car   20 SFO   24 70.0% :heavy_check_mark: | CAR   31 sfo   18 0.0% :x:                  | 13-51
cle   19 NWE   27 81.0% :heavy_check_mark: | cle   33 NWE   36 100.0% :heavy_check_mark: | 13-27
den   19 clt   25 48.0%                    | den   11 CLT   28 91.0% :heavy_check_mark:  | 13-15
gnb   26 KAN   26 90.0% :x:                | gnb   12 KAN   32 98.0% :x:                 | 31-24
mia   18 PIT   24 65.0% :heavy_check_mark: | mia   40 pit   26 44.0% :x:                 | 14-27

First set of predictions for 2019 week 7 (other runs will give
different results) (the Miami-Buffalo prediction looks particularly
ridiculous):

model2                 | actual
---------------------- | ------
kan   9  DEN   22  :x: | 30-6
mia   54 *BUF*  9  :x: | 21-31
ram   36 ATL   28      | 37-10
sfo   26 WAS    8      | 9-0
crd   30 NYG   22      | 27-21
RAI   13 gnb   24      | 24-42
min   33 DET   33      | 42-30
HTX   40 clt   48      | 23-30
JAX   6  cin   13  :x: | 27-17
sdg   27 *OTI* 20  :x: | 20-23
nor   44 CHI   27      | 36-25
*RAV* 24 sea   35  :x: | 30-16
PHI   20 dal   15  :x: | 10-37
*NWE* 61 nyj   16      | 33-0
