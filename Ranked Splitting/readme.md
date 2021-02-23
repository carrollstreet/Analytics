# Ранжированное деление выборок
Когда выборка состоит из огромного множества подгрупп (отличающегося размера), каждая из которых обладает специфичной формой поведения 
(к примеру собирает разное число посещений), для создания тестовой и контрольной групп может быть недостаточно случайного разделения, поскольку оно не гарантирует 
стратификацию, а значит репрезентативность данных, как и эквивалентность обеих групп до начала тестирования.

Если страты сформированы заранее, то проблема решается достаточно просто при помощи модуля `sklearn.model_selection` функцией `train_test_split`, с аргументом stratify. 
Если же страты не сформированы, можно попробовать создать их при помощи кластеризации (например KMeans), либо ранжирования, о котором речь и пойдет. 
Для этого необходимо отсортировать данные по убыванию целевого признака, 
присвоить каждому значению ранг (или индекс), затем разделить данные по рангу на N равных частей при помощи остатка от деления, далее N будет размером подгруппы. 
Размер подгруппы по большому счету будет зависеть от дисперсии в выборке, то есть, чем больше дисперсия, тем меньше подгруппа, 
оптимальный размер можно подобрать эмпирическим путём. После деления данные заново ранжируются и обратно смерживаются. Таким образом получится изначальный датасет, 
где рядом стоящие значения будут иметь одинаковый ранг, с размером подгруппы N. После этого можно воспользоваться известной функцией `train_test_split` и стратифицировать
данные по рангам. Проиллюстрирую принцип работы на очень упрощенном примере:

Представим, что у нас есть записи со значениями от 1 до 100. Далее, присваиваем каждой записи ранг и делим их на 10 подгрупп: 
```python
d = {}
for i in range(100):
    try:
        d[i%10].append(i)
    except KeyError:
        d[i%10] = []
        d[i%10].append(i)
        
>>> {0: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90],
     1: [1, 11, 21, 31, 41, 51, 61, 71, 81, 91],
     2: [2, 12, 22, 32, 42, 52, 62, 72, 82, 92],
                        ...
     8: [8, 18, 28, 38, 48, 58, 68, 78, 88, 98],
     9: [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]}
```
Каждую подгруппу заново ранжируем:
```python
f = d.copy()
for i in f:
    f[i] = list(range(len(d[i])))
    
>>> {0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
     1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
     2: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    ...
     8: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
     9: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
 ```
 Теперь склеиваем все выборки в одну. Таким образом, нулевой ранг будут иметь все записи от 0 до 9, первый от 10 до 19 и так далее. 
 Из каждой подгруппы будем случайно извлечем две выборки, суммарным размером в 20% от размера датасета и сравним их средние:
 ```python
data = np.array(list(d.values())).T
sample = (np.array([np.random.choice(data[i], size=2, replace=False) for i in f]))

print(sample.T)
>>> array([[ 4, 18, 23, 38, 46, 56, 61, 76, 81, 91],
           [ 6, 12, 21, 31, 40, 54, 64, 79, 82, 98]])
           
print(np.mean(sample, axis=0))
>>> array([49.4, 48.7])
  ```
 Сравнение с абсолютно случайным делением:
```python
random_sample1 = np.random.choice(some_data, size=10, replace=False)
random_sample2 = np.random.choice(list(set(some_data).difference(set(random_sample1))), size=10, replace=False)

>>> array([46,  3, 59,  1, 38, 17, 35, 52, 10, 64])
    array([18, 68, 74, 44, 58, 56, 20, 48, 55,  2])
    
>>> array([32.5, 44.3])
```
 
 