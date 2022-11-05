from django.shortcuts import render, redirect
from BMS.models import BookKeep
from django.db.models import Q, Max, Min, Avg, Sum, Count
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    contain = {}
    contain['allData'] = BookKeep.myObjects.all_records_filter()
    contain['pub'] = BookKeep.myObjects.duplicate_tbook()
    contain['add_permission'] = request.user.has_perm('BMS.add_bookkeep')
    contain['update_permission'] = request.user.has_perm('BMS.change_bookkeep')
    contain['delete_permission'] = request.user.has_perm('BMS.delete_bookkeep')
    return render(request, 'BMS/index.html', contain)

def search(request):
    if (request.method == 'POST' and 'search-btn' in request.POST):
        searched = request.POST['search-btn']
        Q1 = Q(author__icontains = searched)
        Q2 = Q(book__icontains = searched)
        Q3 = Q(tbook__icontains = searched)
        context = {}
        context['search'] = searched
        context['allsearch'] = BookKeep.myObjects.filter(Q1 | Q2 | Q3)
        return render(request, 'BMS/search.html', context)
    else:
        return redirect('/')

def filter(request):
    if (request.method == 'POST' and 'filter-btn' in request.POST):
        price_filter = request.POST['price']
        page_filter = request.POST['pages']
        tbook_filter = request.POST['tbook']
        author_filter = request.POST['author']
        context = {}
        context['pub'] = BookKeep.myObjects.duplicate_tbook()
        tbook_check=[]
        for dp in context['pub']:
            for n in dp:
                tbook_check.append(n)
        if (tbook_filter in tbook_check and price_filter == 'htol'):
            context['allData'] = BookKeep.myObjects.desc_by_price_pub(tbook_filter)
        elif (tbook_filter in tbook_check and price_filter == 'ltoh'):
            context['allData'] = BookKeep.myObjects.asc_by_price_pub(tbook_filter)
        elif (tbook_filter in tbook_check and page_filter == 'htol'):
            context['allData'] = BookKeep.myObjects.desc_by_pages_pub(tbook_filter)
        elif (tbook_filter in tbook_check and page_filter == 'ltoh'):
            context['allData'] = BookKeep.myObjects.asc_by_pages_pub(tbook_filter)
        elif (price_filter == 'htol'):
            context['allData'] = BookKeep.myObjects.desc_by_price()
        elif (price_filter == 'ltoh'):
            context['allData'] = BookKeep.myObjects.asc_by_price()
        elif (author_filter == 'htol'):
            context['allData'] = BookKeep.myObjects.desc_by_author()
        elif (author_filter == 'ltoh'):
            context['allData'] = BookKeep.myObjects.asc_by_author()
        elif (page_filter == 'htol'):
            context['allData'] = BookKeep.myObjects.desc_by_pages()
        elif (page_filter == 'ltoh'):
            context['allData'] = BookKeep.myObjects.asc_by_pages()
        elif (tbook_filter in tbook_check):
            context['allData'] = BookKeep.myObjects.tbook_name(tbook_filter)
        else:
            return redirect('/')
        return render(request,'BMS/filter.html',context)
    else:
        return redirect('/')

def add(request):
    if (request.method == 'POST'):
        book = request.POST['bookname']
        author = request.POST['author']
        price = request.POST['price']
        pages = request.POST['pages']
        tbook = request.POST['tbook']

        insert_data = BookKeep.myObjects.create(book = book, author = author, price = price, pages = pages, tbook = tbook)
        insert_data.save()
        return redirect('/')
    return render(request, 'BMS/addBook.html')

def delete(request, bid):
    if request.user.is_authenticated:
        if request.user.has_perm('BMS.delete_bookkeep'):
            delete_data = BookKeep.myObjects.records_by_id(bid)
            delete_data.update(is_deleted = 'y')
            return redirect('/')
        else:
            messages.error(request,'Acess Denied')
            return redirect('/')
    else:
        messages.error(request,'Acess Denied')
        return redirect('/')

def edit(request, bid):
    if (request.method == 'POST'):
        book = request.POST['bookname']
        author = request.POST['author']
        price = request.POST['price']
        pages = request.POST['pages']
        tbook = request.POST['tbook']

        edit_data = BookKeep.myObjects.records_by_id(bid)
        edit_data.update(book = book, author = author, price = price, pages = pages, tbook = tbook)
        return redirect('/')

    else:
        contant = {}
        contant['edit_data'] = BookKeep.myObjects.records_by_id(bid)
        return render(request, 'BMS/updateBook.html',contant)
