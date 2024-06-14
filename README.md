<h1>Pika instead of Celery</h1>

<p>First of all read this article and after that "pip uninstall celery"</p>
<a href='https://ayushshanker.com/posts/celery-in-production-bugfixes'>Article</a>
<p>I faced many problems with celery module, therefore i read many articles and researched for the appropriate solution for that, finally i found out that we as developers cannot control the behaviors of Celery and we can rely on pika and it's advantages.</p>
<p>We can create work queues with persistent messages, We also can use it's perfect features for pub/sub and microservices architecture and many other advantages...</p>
