[simpleaws](https://newsletter.simpleaws.dev/p/aws-lambda-underlying-architecture)

# execution environment
- lambda runs code in **isolated** environment inside micro VM (using Firecracker), allocated in lambda worker (eg. EC2, ...)
- an execution environment will **only be used by one** concurrent invocation