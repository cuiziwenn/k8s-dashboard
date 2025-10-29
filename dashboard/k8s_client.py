from kubernetes import client, config
from kubernetes.client.rest import ApiException
import os

class K8sClient:
    def __init__(self):
        try:
            if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/token'):
                config.load_incluster_config()
            else:
                config.load_kube_config()
            
            self.core_v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
            self.networking_v1 = client.NetworkingV1Api()
        except Exception as e:
            print(f"K8s client initialization error: {e}")
            raise

    # Namespace operations
    def list_namespaces(self):
        try:
            return self.core_v1.list_namespace().items
        except ApiException as e:
            return []

    def create_namespace(self, name):
        body = client.V1Namespace(metadata=client.V1ObjectMeta(name=name))
        return self.core_v1.create_namespace(body)

    def delete_namespace(self, name):
        return self.core_v1.delete_namespace(name)

    # Deployment operations
    def list_deployments(self, namespace='default'):
        try:
            return self.apps_v1.list_namespaced_deployment(namespace).items
        except ApiException:
            return []

    def get_deployment(self, name, namespace='default'):
        return self.apps_v1.read_namespaced_deployment(name, namespace)

    def create_deployment(self, namespace, body):
        return self.apps_v1.create_namespaced_deployment(namespace, body)

    def update_deployment(self, name, namespace, body):
        return self.apps_v1.patch_namespaced_deployment(name, namespace, body)

    def delete_deployment(self, name, namespace='default'):
        return self.apps_v1.delete_namespaced_deployment(name, namespace)

    # Pod operations
    def list_pods(self, namespace='default'):
        try:
            return self.core_v1.list_namespaced_pod(namespace).items
        except ApiException:
            return []

    def get_pod(self, name, namespace='default'):
        return self.core_v1.read_namespaced_pod(name, namespace)

    def delete_pod(self, name, namespace='default'):
        return self.core_v1.delete_namespaced_pod(name, namespace)

    # Service operations
    def list_services(self, namespace='default'):
        try:
            return self.core_v1.list_namespaced_service(namespace).items
        except ApiException:
            return []

    def get_service(self, name, namespace='default'):
        return self.core_v1.read_namespaced_service(name, namespace)

    def create_service(self, namespace, body):
        return self.core_v1.create_namespaced_service(namespace, body)

    def update_service(self, name, namespace, body):
        return self.core_v1.patch_namespaced_service(name, namespace, body)

    def delete_service(self, name, namespace='default'):
        return self.core_v1.delete_namespaced_service(name, namespace)

    # PVC operations
    def list_pvcs(self, namespace='default'):
        try:
            return self.core_v1.list_namespaced_persistent_volume_claim(namespace).items
        except ApiException:
            return []

    def create_pvc(self, namespace, body):
        return self.core_v1.create_namespaced_persistent_volume_claim(namespace, body)

    def delete_pvc(self, name, namespace='default'):
        return self.core_v1.delete_namespaced_persistent_volume_claim(name, namespace)

    # PV operations
    def list_pvs(self):
        try:
            return self.core_v1.list_persistent_volume().items
        except ApiException:
            return []

    def create_pv(self, body):
        return self.core_v1.create_persistent_volume(body)

    def delete_pv(self, name):
        return self.core_v1.delete_persistent_volume(name)

    # Ingress operations
    def list_ingresses(self, namespace='default'):
        try:
            return self.networking_v1.list_namespaced_ingress(namespace).items
        except ApiException:
            return []

    def create_ingress(self, namespace, body):
        return self.networking_v1.create_namespaced_ingress(namespace, body)

    def delete_ingress(self, name, namespace='default'):
        return self.networking_v1.delete_namespaced_ingress(name, namespace)

    # Cluster metrics
    def get_cluster_metrics(self):
        import psutil
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory()._asdict(),
            'disk': psutil.disk_usage('/')._asdict()
        }