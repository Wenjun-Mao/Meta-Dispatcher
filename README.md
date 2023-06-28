# Meta-Dispatcher
Meta-Dispatcher to multiple internal services. Internal service(s) could alreay be a dispatcher to other internal services.
Global lock is implemented to limit the number of concurrent requests to internal services to always one at a time. This is due to some internal services could conflict on CUDA resources.
