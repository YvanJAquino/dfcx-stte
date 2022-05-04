# Speech-to-text Extension Modules

## matcher.py: The Name [Noun] Matcher
matcher.py serves two purposes: (a) it defines the AI/ML pipeline that converts a list of names into a name matching service and (b) it provides a command-line interface for model creation and re-creation.

The matching service pipeline consists of:
- Accessing the list of names,
- Compiling the list of names into a Vectorized TF-IDF model
- Applying kNN with cosine similarity as the metric
- delivering the final name matching solution which accepts a name and returns a sorted list of high similarity names from the name list.

```python
   def match(self, target: str):
      vectorized = self.vectorizer.transform([target]) # transforming to the target
      distances, indices = self.kneighbors.kneighbors(vectorized) # performing kNN
      
      # dict was chosen for ease of use.  
      # A NamedTuple might work equally well - at the added expense of 
      # extra manageability.
      records = [
         {
            'target':target,
            'source': self.source[idx],
            'similarity': 1-dist.item()
         }
         for dist, idx in zip(distances[0], indices[0])
      ]
      records.sort(key=lambda d: d['similarity'], reverse=True)
      return records # return list of records 
```

Instead of training the model during runtime, the model is trained by Cloud Build during the build-time definition of the container.  Every time the container is redeployed, the model is re-built.  

## models.py, whr_client.py: Pydantic WebhookRequest and WebhookResponse class definitions
models.py and whr_client.py are class based 'basic' representations of the WebhookRequest and WebhookResponse objects.  It's the authors desire to implement both WebhookRequest and WebhookResponse - but there are only so many hours in the day.  

The WebhookResponse (whr_client.py) objects have been extended with methods to make creating, updating, and adding to WebhookResponse objects cleaner.

### Preparing a text response without whr_client.py
```python
# Ouch, this hurts my brain...
def text_response(text: str) -> dict:
        return {
        'fulfillment_response': {
            'messages': [
                {
                    'text': {
                        'text': [
                            text
                        ]
                    }
                }
            ]
        }
    }
```
### Preparing a text response WITH whr_client.py
```python
# Awww yeaahhh...
response = WebhookResponse()
response.add_text_response("Your message(s) go here.")
response.add_session_params({"i-can-add-session-params": True})

# with FastApi, you can just return response.
# Alternatively, response.to_dict() returns a dictionary that excludes
# unused keys to reduce wire traffic.
```


## stringpipe.py: String Pipes - A String Operations and Pipeline Library
String Pipes is a small library that aims to make string based manipulations easier to read and maintain.  

The String Pipes syntax is inspired by Apache Beam.   

### Without Stringpipe

```python
def to_cum_ngrams(inp: str, m = 2, n, = 3):

    """
        n (maximum ngram size, default = 3, trigram)
        m (minimum ngram size, default = 2, digram)
    """

    if not isinstance(inp, str):
        try:
            # Attempt to coerce to string
            inp = str(inp)
        except Exception as e:
            print(f'Oops: {e}!')
    
    res = set()
    inp = inp.lower()
    table = str.maketrans('', '', string.punctuation)
    inp = inp.translate(table)
    tri = {inp[i:i+n] for i in range(len(inp)-(n-1))}
    di = {inp[i:i+m] for i in range(len(inp)-(m-1))}
    return tri.union(di)
    
```

### With Stringpipe
```python
# When used within a context manager, the StringPipeline class
# returns a Pipeline instance as well as an StringOperators instance
def cum_ngrams():
    with StringPipeline() as (pipe, ops):
        (
            pipe
                >> ops.str()                # coerce to string
                >> ops.lower()              # convert all to lower case
                >> ops.remove_punctuation() # remove all punctuation
                >> ops.cum_ngrams()         # return set of di-, tri-grams.
        )
        return pipe # Returns a callable that accepts the input string.
```

If, at any point in the pipeline, the string is converted into an iterable (such as a list), String Pipes applies the transforms on an elementwise basis instead. 

### without Stringpipe
```python
sample = "Hello World"
transformed = sample.split(" ") # ['Hello', 'World']
transformed = [word.lower() for word in transformed] # ['hello', 'world']
transformed = [word[::-1] for word in transformed] # ['olleh', 'dlrow']
transformed = "".join(transformed) # 'ollehdlrow'
```
### With Stringpipe
```python
sample = "Hello World"
with StringPipeline() as (pipe, ops): 
    # both pipe and ops are available in global namespace.
    (
        pipe
            >> ops.split()      # ['Hello', 'World'], default= " "
            >> ops.lower()      # ['hello', 'world']
            >> ops.reverse()    # ['olleh', 'dlrow']
            >> ops.join()       # 'ollehdlrow', default = ""
    )
result = pipe(sample) # 'ollehdlrow'
```