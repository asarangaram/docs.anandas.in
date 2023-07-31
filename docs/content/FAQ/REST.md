---
title: REST FAQ
weight: 611000
---
#  REST API

Can we use query-parameters in RESTful API?

> In the REST architecture, query parameters are commonly used with GET requests to filter, sort, or paginate the data being retrieved. 
>
>  POST, PATCH, and DELETE requests are considered to be more focused on modifying or deleting resources rather than retrieving them. In these cases, the data associated with the request is usually sent in the request body, rather than as query parameters in the URL.
> 
> However, there may be certain situations where you want to include additional parameters in the URL for POST, PATCH, or DELETE requests. It might be used to specify a resource ID or other specific details related to the request. However, using query parameters in these requests is not a widely adopted practice and can go against the principles of RESTful design.