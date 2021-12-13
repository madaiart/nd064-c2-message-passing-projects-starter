# Kafka execution on kubernetes
For this project the kafka kubernetes must be installed on the host
## Installation
To deploy a Kafka in kubernetes, follow the steps below:

1. Install helm (at least version 3.2.1)
    
    ```
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    
    chmod 700 get_helm.sh
  
   ./get_helm.sh
    ```

2. Include the helm repo from bitnami

    ```
    helm repo add bitnami https://charts.bitnami.com/bitnami
    ```

3. Run helm kafka-release
    
    ```
    helm install kafka-release bitnami/kafka
    ``` 

------
Common output when kafka is installed

```
NAME: kafka-release
LAST DEPLOYED: Sun Dec 12 19:51:44 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: kafka
CHART VERSION: 14.5.1
APP VERSION: 2.8.1

** Please be patient while the chart is being deployed **

Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

    kafka-release.default.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    kafka-release-0.kafka-release-headless.default.svc.cluster.local:9092

To create a pod that you can use as a Kafka client run the following commands:

    kubectl run kafka-release-client --restart='Never' --image docker.io/bitnami/kafka:2.8.1-debian-10-r57 --namespace default --command -- sleep infinity

    kubectl exec --tty -i kafka-release-client --namespace default -- bash

    PRODUCER:
        kafka-console-producer.sh \            
            --broker-list kafka-release-0.kafka-release-headless.default.svc.cluster.local:9092 \
            --topic test

    CONSUMER:
        kafka-console-consumer.sh \            
            --bootstrap-server kafka-release.default.svc.cluster.local:9092 \
            --topic test \
            --from-beginning
```