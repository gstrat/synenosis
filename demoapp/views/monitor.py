from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic.base import View
from synenosis.tasks import import_winbank, import_nbg, import_paypal
from ..forms.accounts import AddWinbankAccountForm, AddNBGAccountForm, \
        AddPayPalAccountForm


class ProgressMonitorView(View):
    """ A view that returns the task state """
    def get(self, request, *args, **kwargs):
        job_id = request.GET.get('job')

        from django_project.celery import app
        try:
            job = app.AsyncResult(job_id)
        except:
            return HttpResponseBadRequest()

        if job.state == 'SUCCESS':
            try:
                fmessage = job.info.get('fmessage')
            except:
                result = {'message': 'The process has finished.',
                          'progress': 100}
            else:
                # the task has actually failed but we caught the exception to
                # display an appropriate message to the user
                result = {'error': 1, 'message': fmessage}
        elif job.state == 'PENDING':
            result = {'message': 'Waiting for the importer to start...',
                      'progress': 3}
        elif job.state == 'STARTED':
            result = {'message': 'The import has started.',
                      'progress': 5}
        elif job.state == 'FAILURE':
            result = {'error': 1,
                      'message': 'The import has failed. Please retry later.'}
        elif job.state == 'PROGRESS':
            message = job.info.get('message')
            progress = job.info.get('progress')
            result = {'message': message, 'progress': progress}
        else:
            result = {'message': 'The import state is unknown...'}

        return JsonResponse(result)

class BaseQueueView(View):
    task_name = None

    def get_task_name(self):
        """ Get the task name """
        return self.task_name

    def get_response(self):
        """ Get the response after the job is queued """
        return JsonResponse({'job_id': self.job.id,
                             'message': 'Initializing...',
                             'progress': 2,
                             'task_name': self.get_task_name()})

    def queue_job(self):
        """ Queue and return the job """
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=self.request.POST)
        if form.is_valid():
            self.job = self.queue_job(form.data)
            return self.get_response()
        else:
            return HttpResponseBadRequest()


class ImportWinbankQueue(BaseQueueView):
    task_name = 'import_winbank'
    form_class = AddWinbankAccountForm

    def queue_job(self, data):
        return import_winbank.delay( # @UndefinedVariable
            username=data.get('username'), 
            password=data.get('password'),
            number=data.get('number'))


class ImportNBGQueue(BaseQueueView):
    task_name = 'import_nbg'
    form_class = AddNBGAccountForm

    def queue_job(self, data):
        return import_nbg.delay( # @UndefinedVariable
            key=data.get('key'), 
            account_id=data.get('account_id'))


class ImportPayPalQueue(BaseQueueView):
    task_name = 'import_paypal'
    form_class = AddPayPalAccountForm

    def queue_job(self, data):
        return import_paypal.delay( # @UndefinedVariable
            username=data.get('paypal_username'),
            password=data.get('paypal_password'),
            signature=data.get('signature')
        )
