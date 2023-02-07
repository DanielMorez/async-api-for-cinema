FROM openkbs/jre-mvn-py3:latest

RUN pip install jupyter pyspark==3.0.1

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]