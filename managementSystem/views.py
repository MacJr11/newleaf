from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



def register_client(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_email = request.POST.get('contact_email')
        phone = request.POST.get('phone')

        if client_id:
            client = get_object_or_404(Client, id=client_id)
            client.name = name
            client.phone = phone
            client.address = address
            client.email = contact_email
            client.save()
            return JsonResponse({'success': True, 'message': 'Worker updated successfully!'})
        else:
        # Basic validation example
            if name and contact_email:
                Client.objects.create(
                    name=name,
                    address=address,
                    contact_email=contact_email,
                    phone=phone,
                )
                return JsonResponse({'success': True, 'message': 'Worker added successfully!'})
            else:
                error = "Name and Email are required."
                return JsonResponse({'success': True, 'message': error})
    
    clients = Client.objects.all().order_by('-id')
    paginator = Paginator(clients, 10)  # 10 workers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'register_client.html', {
        'clients': page_obj,
        'paginator': paginator,
        'page_obj': page_obj,
    })
    

def get_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    data = {
        'id': client.id,
        'name': client.name,
        'phone': client.phone,
        'email': client.contact_email,
        'address': client.address,
    }
    return JsonResponse(data)

@require_POST
def client_delete(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        client.delete()
        return JsonResponse({'success': True, 'message': 'Client deleted successfully!'})
    except Client.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Client not found.'}, status=404)
    
def create_order(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        po_number = request.POST.get('po_number')
        date = request.POST.get('date')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status', 'Pending')

        if po_number and date and due_date:
            order = PurchaseOrder.objects.create(
                po_number=po_number,
                client=client,
                date=date,
                due_date=due_date,
                status=status
            )
            return redirect('order_detail', order_id=order.id)  # You can implement this view later
        else:
            error = "Please fill all required fields."
            return render(request, 'create_order.html', {'client': client, 'error': error})

    return render(request, 'create_order.html', {'client': client})
