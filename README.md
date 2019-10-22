This is an exercise in learning how to use Keras/TensorFlow.

I really don't know what I'm doing.  I'm mostly blindly following the
examples in the documentation without knowing what most of the
terminology is or what most of the parameters mean.

First set of predictions for 2019 week 8 (model1 tends to pick San
Francisco over Carolina, while model2 consistently picks Carolina over
San Francisco.  For the Thursday game, model2 consistently projects
Minnesota to score around 40 and to win by around 20 over Washington.
model1 and model2 also like Seattle and New Orleans):

model1                                              | model2                                              | actual
--------------------------------------------------- | --------------------------------------------------- | ------
<pre style="color:#000;">was 16 MIN 29 98.0%</pre>  | <pre style="color:#000;">was 21 MIN 41 100.0%</pre> |
<pre style="color:#000;">sdg 21 chi 24 55.0%</pre>  | <pre style="color:#000;">SDG 23 chi 27 15.0%</pre>  |
<pre style="color:#000;">phi 18 buf 24 40.0%</pre>  | <pre style="color:#000;">phi 11 BUF 20 77.0%</pre>  |
<pre style="color:#000;">sea 27 atl 20 56.0%</pre>  | <pre style="color:#000;">SEA 39 atl 14 0.0%</pre>   |
<pre style="color:#000;">cin 19 RAM 25 63.0%</pre>  | <pre style="color:#000;">CIN 23 ram 19 26.0%</pre>  |
<pre style="color:#000;">TAM 23 oti 23 32.0%</pre>  | <pre style="color:#000;">TAM 20 oti 21 7.0%</pre>   |
<pre style="color:#000;">crd 18 NOR 25 83.0%</pre>  | <pre style="color:#000;">crd 14 NOR 23 100.0%</pre> |
<pre style="color:#000;">nyj 17 JAX 27 100.0%</pre> | <pre style="color:#000;">nyj 15 JAX 32 65.0%</pre>  |
<pre style="color:#000;">rai 21 HTX 28 65.0%</pre>  | <pre style="color:#000;">RAI 22 htx 22 32.0%</pre>  |
<pre style="color:#000;">nyg 19 DET 23 75.0%</pre>  | <pre style="color:#000;">nyg 18 DET 19 95.0%</pre>  |
<pre style="color:#000;">car 20 SFO 24 70.0%</pre>  | <pre style="color:#000;">CAR 31 sfo 18 0.0%</pre>   |
<pre style="color:#000;">cle 19 NWE 27 81.0%</pre>  | <pre style="color:#000;">cle 33 NWE 36 100.0%</pre> |
<pre style="color:#000;">den 19 clt 25 48.0%</pre>  | <pre style="color:#000;">den 11 CLT 28 91.0%</pre>  |
<pre style="color:#000;">gnb 26 KAN 26 90.0%</pre>  | <pre style="color:#000;">gnb 12 KAN 32 98.0%</pre>  |

First set of predictions for 2019 week 7 (other runs will give
different results) (the Miami-Buffalo prediction looks particularly
ridiculous):

model2                                       | actual
-------------------------------------------- | ------
<pre style="color:#f00;">kan 9 DEN 22</pre>  | 30-6
<pre style="color:#f00;">mia 54 BUF 9</pre>  | 21-31
<pre style="color:#000;">ram 36 ATL 28</pre> | 37-10
<pre style="color:#000;">sfo 26 WAS 8</pre>  | 9-0
<pre style="color:#000;">crd 30 NYG 22</pre> | 27-21
<pre style="color:#000;">RAI 13 gnb 24</pre> | 24-42
<pre style="color:#f00;">min 33 DET 33</pre> | 42-30
<pre style="color:#000;">HTX 40 clt 48</pre> | 23-30
<pre style="color:#f00;">JAX 6 cin 13</pre>  | 27-17
<pre style="color:#f00;">sdg 27 OTI 20</pre> | 20-23
<pre style="color:#000;">nor 44 CHI 27</pre> | 36-25
<pre style="color:#f00;">RAV 24 sea 35</pre> | 30-16
<pre style="color:#f00;">PHI 20 dal 15</pre> | 10-37
<pre style="color:#0f0;">NWE 61 nyj 16</pre> | 33-0
