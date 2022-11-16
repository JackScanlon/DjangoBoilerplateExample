import json
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from datetime import datetime
from django.urls import reverse
from elasticsearch_dsl import Q
from .models import Post
from .documents import PostDocument

class PostsCreatorView(TemplateView):
    template_name = 'posts/create.html'

    def get(self, request):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account_login'))
        
        return render(request, self.template_name, None)
    
    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account_login'))
        
        ctx = {'created': False}
        req_body = self.request.body.decode('utf-8')
        try:
            packet = json.loads(req_body)
            title = packet['title']
            content = packet['content']
            user_id = self.request.user.id
            created = datetime.now()

            post = Post(
                title=title,
                user_id=user_id,
                content=content,
                created_at=created
            )
            post.save()
            ctx = {'slug': post.slug, 'created': True}
        except:
            pass

        return JsonResponse(ctx)
        

class PostsSearchView(TemplateView):
    template_name = 'posts/index.html'

    def get_recent_posts(self, context):
        context['results'] = Post.objects.order_by('-created_at')[:9]

    def run_query(run_query, search_query, context):
        query = Q({'multi_match': {'query': search_query, 'fields': ['title', 'content'], 'fuzziness': 1}})
        search = PostDocument.search().query(query).to_queryset()
        if search.count() > 0:
            context['has_results'] = True
            context['results'] = search

    def post(self, request, *args, **kwargs):
        context = {'has_results': False}
        packet = { }
        req_body = self.request.body.decode('utf-8')

        try:
            packet = json.loads(req_body)
            if 'query' in packet:
                search_query = packet['query']
                if len(search_query) <= 0:
                    self.get_recent_posts(context)
                else:
                    self.run_query(search_query, context)
        except:
            pass
        
        if 'results' in context:
            context['results'] = list(context['results'].values())
        
        return JsonResponse(context)


    def get(self, request, *args, **kwargs):
        context = { }
        
        search_query = self.request.GET.get('query', '')
        if len(search_query) > 0:
            self.run_query(search_query, context)
        else:
            self.get_recent_posts(context)

        created_slug = kwargs.get('slug', None)
        if created_slug:
            context['created_post'] = True
            context['slug'] = created_slug
        
        return render(request, self.template_name, context)