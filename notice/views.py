from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView
from notice.models import Employee,User,Notice
from django.contrib import messages
from django.db.models import Q
from .forms import NoticeWriteForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required



# Create your views here.
class NoticeListView(ListView):
    model = Notice
    paginate_by = 10
    template_name = 'notice/notice_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'notice_list'        #DEFAULT : <model_name>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        notice_list = Notice.objects.order_by('-not_id')

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_notice_list = notice_list.filter(
                        Q(not_title__icontains=search_keyword) | Q(not_content__icontains=search_keyword) | Q(not_writer__user_email__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_notice_list = notice_list.filter(
                        Q(not_title__icontains=search_keyword) | Q(not_content__icontains=search_keyword))
                elif search_type == 'title':
                    search_notice_list = notice_list.filter(not_title__icontains=search_keyword)
                elif search_type == 'content':
                    search_notice_list = notice_list.filter(not_content__icontains=search_keyword)
                elif search_type == 'writer':
                    search_notice_list = notice_list.filter(not_writer__user_email__icontains=search_keyword)

                return search_notice_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return notice_list
#JS로 서버 // 이건 py라서 admin 페이지에 경고가 뜸// html -> alret

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type



        return context


def notice_detail_view(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    user = request.user
    email = user.email
    writer = Employee.objects.get(emp_email=email)

    if user == writer:
        notice_auth = True
    else:
        notice_auth = False

    context = {
        'notice': notice,
        'notice_auth':notice_auth,
    }
    return render(request, 'notice/notice_detail.html', context)

@login_required
def notice_write_view(request):
    if request.method == "POST":
        form = NoticeWriteForm(request.POST)
        user = request.user
        email = user.email
        writer = Employee.objects.get(emp_email=email)

        if form.is_valid():
            notice = form.save(commit = False)
            notice.not_writer = writer
            notice.save()
            return redirect('notice_list')
    else:
        form = NoticeWriteForm()
    return render(request, "notice/notice_write.html", {'form': form})


@login_required
def notice_edit_view(request, pk):
    notice = Notice.objects.get(not_id=pk)
    user = request.user
    email = user.email
    writer = Employee.objects.get(emp_email=email)

    if request.method == "POST":
        if (notice.not_writer == writer or user.username == 'boss'):
            form = NoticeWriteForm(request.POST, instance=notice)
            if form.is_valid():
                notice = form.save(commit=False)
                notice.save()
                messages.success(request, "수정되었습니다.")
                return redirect('/notice/' + str(pk))
    else:
        notice = Notice.objects.get(not_id=pk)
        if (notice.not_writer == writer or user.username == 'boss'):
            form = NoticeWriteForm(instance=notice)
            context = {
                'form': form,
                'edit': '수정하기',
            }
            return render(request, "notice/notice_write.html", context)
        else:
            messages.error(request, "본인 게시글이 아닙니다.")





            return redirect('/notice/' + str(pk))

@login_required
def notice_delete_view(request, pk):
    notice = Notice.objects.get(not_id=pk)
    user = request.user
    email = user.email
    writer = Employee.objects.get(emp_email=email)

    if (notice.not_writer == writer or user.username == 'boss'):
        notice.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('/notice/')
    else:
        messages.error(request, "본인 게시글이 아닙니다.")
        return redirect('/notice/'+str(pk))

