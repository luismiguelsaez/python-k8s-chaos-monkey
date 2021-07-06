from kubernetes import client, config
from os import getenv
from sys import exit
from time import sleep

def main():

    try:
      config.load_incluster_config()
    except config.config_exception.ConfigException as k_exc:
      print("Kubernetes API not reachable! Exiting application ...")
      exit(1)

    namespace = getenv('CM_NAMESPACE')

    print("Getting pods from namespace [%s]" % namespace)

    v1 = client.CoreV1Api()

    while True:
      try:
        pod_list = v1.list_namespaced_pod(namespace=namespace)
      except client.exceptions.ApiException as p_exec:
        print("Insuficient permissions while trying to get pods from namespace [%s]! Exiting ..." % namespace)
        exit(1)

      print("Got resources of type [%s]" % pod_list.kind)

      for pod in pod_list.items:
          print("%s\t%s\t%s" % (pod.metadata.name, pod.status.phase, pod.status.pod_ip))

      sleep(1)


if __name__ == '__main__':
    main()
