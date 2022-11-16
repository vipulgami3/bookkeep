from django.shortcuts import render, redirect
from BMS.models import BookKeep
from django.db.models import Q, Max, Min, Avg, Sum, Count
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission, AnonymousUser
from django.core.paginator import Paginator
from django.db.models.manager import EmptyManager
from members.forms import RegisterUser
# Create your views here.

def permissions(request):
    permission = {}
    permission['add_permission'] = request.user.has_perm('BMS.add_bookkeep')
    permission['update_permission'] = request.user.has_perm('BMS.change_bookkeep')
    permission['delete_permission'] = request.user.has_perm('BMS.delete_bookkeep')
    permission['add_user'] = request.user.has_perm('auth.add_user')
    permission['delete_user'] = request.user.has_perm('auth.delete_user')
    permission['change_user'] = request.user.has_perm('auth.change_user')
    permission['view_user'] = request.user.has_perm('auth.view_user')
    permission['change_permission'] = request.user.has_perm('auth.change_permission')
    return permission


def index(request):
    contain = {}
    contain['allData'] = BookKeep.myObjects.all_records_filter()
    contain['pub'] = BookKeep.myObjects.duplicate_tbook()
    p = Paginator(BookKeep.myObjects.all_records_filter(), 10)
    page = request.GET.get('page')
    contain['pageno'] = p.get_page(page)
    contain['nums'] = 'a' * contain['pageno'].paginator.num_pages
    contain['acess_perm'] = permissions(request)
    booklist_user = []
    userbooks = BookKeep.myObjects.filter(user__id=request.user.id)
    for userbook in userbooks :
        booklist_user.append(userbook.book)
    contain['AddedBook'] = booklist_user
    contain['auser'] = request.user.username
    return render(request, 'BMS/index.html', contain)

def search(request):
    if (request.method == 'POST' and 'search-btn' in request.POST):
        searched = request.POST['search-btn']
        Q1 = Q(author__icontains = searched)
        Q2 = Q(book__icontains = searched)
        Q3 = Q(tbook__icontains = searched)
        contain = {}
        contain['search'] = searched
        contain['acess_perm'] = permissions(request)
        contain['allsearch'] = BookKeep.myObjects.all_records_filter().filter(Q1 | Q2 | Q3)
        return render(request, 'BMS/search.html', contain)
    else:
        return redirect('/')

def filter(request):
    if (request.method == 'POST' and 'filter-btn' in request.POST):
        price_filter = request.POST['price']
        page_filter = request.POST['pages']
        tbook_filter = request.POST['tbook']
        author_filter = request.POST['author']
        contain = {}
        contain['pub'] = BookKeep.myObjects.duplicate_tbook()
        contain['acess_perm'] = permissions(request)
        tbook_check=[]
        for dp in contain['pub']:
            for n in dp:
                tbook_check.append(n)
        if (tbook_filter in tbook_check and price_filter == 'htol'):
            contain['allData'] = BookKeep.myObjects.desc_by_price_pub(tbook_filter)
        elif (tbook_filter in tbook_check and price_filter == 'ltoh'):
            contain['allData'] = BookKeep.myObjects.asc_by_price_pub(tbook_filter)
        elif (tbook_filter in tbook_check and page_filter == 'htol'):
            contain['allData'] = BookKeep.myObjects.desc_by_pages_pub(tbook_filter)
        elif (tbook_filter in tbook_check and page_filter == 'ltoh'):
            contain['allData'] = BookKeep.myObjects.asc_by_pages_pub(tbook_filter)
        elif (price_filter == 'htol'):
            contain['allData'] = BookKeep.myObjects.desc_by_price()
        elif (price_filter == 'ltoh'):
            contain['allData'] = BookKeep.myObjects.asc_by_price()
        elif (author_filter == 'htol'):
            contain['allData'] = BookKeep.myObjects.desc_by_author()
        elif (author_filter == 'ltoh'):
            contain['allData'] = BookKeep.myObjects.asc_by_author()
        elif (page_filter == 'htol'):
            contain['allData'] = BookKeep.myObjects.desc_by_pages()
        elif (page_filter == 'ltoh'):
            contain['allData'] = BookKeep.myObjects.asc_by_pages()
        elif (tbook_filter in tbook_check):
            contain['allData'] = BookKeep.myObjects.tbook_name(tbook_filter)
        else:
            return redirect('/')
        return render(request,'BMS/filter.html',contain)
    else:
        return redirect('/')

def add(request):
    if request.user.is_authenticated:
        if (request.method == 'POST'):
            book = request.POST['bookname']
            author = request.POST['author']
            price = request.POST['price']
            pages = request.POST['pages']
            tbook = request.POST['tbook']
            images = request.FILES['images']
            insert_data = BookKeep.myObjects.create(book = book, author = author, price = price, pages = pages, tbook = tbook, images=images)
            insert_data.save()
            return redirect('/')
        else:
            contain = {}
            contain['acess_perm'] = permissions(request)
            return render(request, 'BMS/addBook.html',contain)
    else:
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
    if request.user.is_authenticated:
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
            contain = {}
            contain['acess_perm'] = permissions(request)
            contain['edit_data'] = BookKeep.myObjects.records_by_id(bid)
            return render(request, 'BMS/updateBook.html',contain)
    else:
        return render(request, 'BMS/updateBook.html')

def all_user(request):
    if request.user.is_authenticated:
        if request.user.has_perm('auth.view_user'):
            contain = {}
            contain['acess_perm'] = permissions(request)
            contain['all_user'] = True
            contain['alluser'] = User.objects.filter(is_superuser=False).filter(is_active=True)
            return render(request, 'BMS/all_user.html', contain)
        else:
            return render(request, 'BMS/all_user.html')
    else:
        return redirect('/')

def all_deactive_user(request):
    if request.user.is_authenticated:
        if request.user.has_perm('auth.view_user'):
            contain = {}
            contain['acess_perm'] = permissions(request)
            contain['all_deactive_user'] = True
            contain['alluser'] = User.objects.filter(is_superuser=False).filter(is_active=False)
            return render(request, 'BMS/all_user.html', contain)
        else:
            return render(request, 'BMS/all_user.html')
    else:
        return redirect('/')

def all_superuser(request):
    if request.user.is_authenticated:
        if request.user.has_perm('auth.view_user'):
            contain = {}
            contain['acess_perm'] = permissions(request)
            contain['all_superuser'] = True
            contain['alluser'] = User.objects.filter(is_superuser=True).filter(is_active=True)
            return render(request, 'BMS/all_user.html', contain)
        else:
            return render(request, 'BMS/all_user.html')
    else:
        return redirect('/')

def add_user(request):
    contain = {}
    contain['acess_perm'] = permissions(request)
    if request.user.is_authenticated:
        if request.user.has_perm('auth.add_user'):
            if request.method == 'POST':
                form = RegisterUser(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Registration successfull')
                    return redirect('all_user')
                else:
                    messages.error(request, 'Registration failed')
                    return redirect('add_user')
            else:
                contain['form'] = RegisterUser()
                return render(request, 'BMS/add_user.html', contain)
        else:
            return render(request, 'BMS/add_user.html', contain)
    else:
        return redirect('/')

def deactivated_user(request, uid):
    if request.user.is_authenticated:
        if request.user.has_perm('BMS.delete_user'):
            deactivated_user = User.objects.filter(id = uid)
            deactivated_user.update(is_active = False)
            messages.success(request, f'{deactivated_user[0]} User Deactivated Successfull')
            return redirect('all_user')
        else:
            messages.error(request,'Acess Denied')
            return redirect('/')
    else:
        messages.error(request,'Acess Denied')
        return redirect('/')

def activated_user(request, uid):
    if request.user.is_authenticated:
        if request.user.has_perm('BMS.delete_user'):
            activated_user = User.objects.filter(id = uid)
            activated_user.update(is_active = True)
            messages.success(request, f'{activated_user[0]} User Activated Successfull')
            return redirect('all_deactive_user')
        else:
            messages.error(request,'Acess Denied')
            return redirect('/')
    else:
        messages.error(request,'Acess Denied')
        return redirect('/')

def edit_user(request, uid):
    contain = {}
    contain['acess_perm'] = permissions(request)
    if request.user.is_authenticated:
        if (request.method == 'POST'):
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            is_active = request.POST['is_active']
            update_user = User.objects.filter(id = uid)
            update_user.update(username=username, first_name=first_name, last_name=last_name, email=email, is_active=is_active)
            messages.success(request, f'{username} User Updated Successfull')
            return redirect('all_user')
        else:
            contain['edit_user'] = User.objects.filter(id = uid)
            return render(request, 'BMS/updateUser.html',contain)
    else:
        return render(request, 'BMS/updateUser.html')


def saved_book(request):
    if request.user.is_authenticated:
        contain = {}
        if (request.method == 'POST' and 'filter-btn' in request.POST):
            price_filter = request.POST['price']
            page_filter = request.POST['pages']
            tbook_filter = request.POST['tbook']
            author_filter = request.POST['author']
            contain['pub'] = BookKeep.myObjects.duplicate_tbook()
            tbook_check=[]
            for dp in contain['pub']:
                for n in dp:
                    tbook_check.append(n)
            if (tbook_filter in tbook_check and price_filter == 'htol'):
                contain['AddedBook'] = BookKeep.myObjects.desc_by_price_pub(tbook_filter).filter(user__id=request.user.id)
            elif (tbook_filter in tbook_check and price_filter == 'ltoh'):
                contain['AddedBook'] = BookKeep.myObjects.asc_by_price_pub(tbook_filter).filter(user__id=request.user.id)
            elif (tbook_filter in tbook_check and page_filter == 'htol'):
                contain['AddedBook'] = BookKeep.myObjects.desc_by_pages_pub(tbook_filter).filter(user__id=request.user.id)
            elif (tbook_filter in tbook_check and page_filter == 'ltoh'):
                contain['AddedBook'] = BookKeep.myObjects.asc_by_pages_pub(tbook_filter).filter(user__id=request.user.id)
            elif (price_filter == 'htol'):
                contain['AddedBook'] = BookKeep.myObjects.desc_by_price().filter(user__id=request.user.id)
            elif (price_filter == 'ltoh'):
                contain['AddedBook'] = BookKeep.myObjects.asc_by_price().filter(user__id=request.user.id)
            elif (author_filter == 'htol'):
                contain['AddedBook'] = BookKeep.myObjects.desc_by_author().filter(user__id=request.user.id)
            elif (author_filter == 'ltoh'):
                contain['AddedBook'] = BookKeep.myObjects.asc_by_author().filter(user__id=request.user.id)
            elif (page_filter == 'htol'):
                contain['AddedBook'] = BookKeep.myObjects.desc_by_pages().filter(user__id=request.user.id)
            elif (page_filter == 'ltoh'):
                contain['AddedBook'] = BookKeep.myObjects.asc_by_pages().filter(user__id=request.user.id)
            elif (tbook_filter in tbook_check):
                contain['AddedBook'] = BookKeep.myObjects.tbook_name(tbook_filter).filter(user__id=request.user.id)
            else:
                return redirect('saved_book')
            return render(request, 'BMS/savedbook.html', contain)

        else:
            contain['AddedBook'] = BookKeep.myObjects.filter(user__id=request.user.id)
            return render(request, 'BMS/savedbook.html', contain)
    else:
        return redirect('/')

def saving_book(request, uid):
    if request.user.is_authenticated:
        saving_book = BookKeep.myObjects.get(id = uid)
        saving_book.user.add(request.user.id)
        messages.success(request, f'{saving_book} Book Added Successfull')
        return redirect('/')
    else:
        return redirect('/')

def remove_book(request, uid):
    if request.user.is_authenticated:
        remove_book = BookKeep.myObjects.get(id = uid)
        remove_book.user.clear()
        messages.success(request, f'{remove_book} Book Removed Successfull')
        return redirect('saved_book')
    else:
        return redirect('/')

def user_profile(request, uid):
    if request.user.is_authenticated:
        contain = {}
        contain['user'] = User.objects.get(id = uid)
        return render(request, 'BMS/userprofile.html', contain)
    else:
        return render(request, 'BMS/userprofile.html')

def edit_by_user(request, uid):
    if request.user.is_authenticated:
        if uid == request.user.id:
            if (request.method == 'POST'):
                username = request.POST['username']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                update_user = User.objects.filter(id = uid)
                update_user.update(username=username, first_name=first_name, last_name=last_name, email=email)
                messages.success(request, 'Profile Updated')
                return redirect('user_profile',uid)
            else:
                contain = {}
                contain['editbyuser'] = User.objects.get(id = uid)
                return render(request, 'BMS/editbyuser.html', contain)
        else:
            return render(request, 'BMS/editbyuser.html')
    else:
        return redirect('/')

def permission(request):
    if request.user.is_authenticated:
        contain = {}
        contain['alluserperm'] = User.objects.filter(is_superuser=False).filter(is_active=True)
        return render(request, 'BMS/permission.html', contain)
    else:
        return redirect('/')

def updatepermission(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            add_list = request.POST.getlist('perm')
            update_list = request.POST.getlist('perm1')
            delete_list = request.POST.getlist('perm2')
            add_id_list = ([int(x) for x in add_list])
            update_id_list = ([int(x) for x in update_list])
            delete_id_list = ([int(x) for x in delete_list])
            all_active_user = User.objects.filter(is_superuser=False).filter(is_active=True)
            for q in all_active_user:
                addid = q.id
                if addid in add_id_list:
                    print('add')
                    c = User.objects.filter(id = addid)
                    for i in c:
                        i.user_permissions.add(25)
                else:
                    print("else1")
                    c = User.objects.filter(id = addid)
                    for i in c:
                        i.user_permissions.remove(25)
            for p in all_active_user:
                updateid = p.id
                if updateid in update_id_list:
                    print('update')
                    c = User.objects.filter(id = updateid)
                    for i in c:
                        i.user_permissions.add(26)
                else:
                    print("else2")
                    c = User.objects.filter(id = updateid)
                    for i in c:
                        i.user_permissions.remove(26)
            for r in all_active_user:
                deleteid = r.id
                if deleteid in delete_id_list:
                    print('delete')
                    c = User.objects.filter(id = deleteid)
                    for i in c:
                        i.user_permissions.add(27)
                else:
                    print("else3")
                    c = User.objects.filter(id = deleteid)
                    for i in c:
                        i.user_permissions.remove(27)
            return redirect('permission')
        else:
            contain = {}
            contain['alluserperm'] = User.objects.filter(is_superuser=False).filter(is_active=True)
            return render(request, 'BMS/updatepermission.html', contain)
    else:
        return redirect('/')
