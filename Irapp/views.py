# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .main import initialize_ir_system, do_search, document_filenames
import os  # Ensure this import is present

# Initialize the IR system once at the start
initialize_ir_system()

def search(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        if query:
            results = do_search(query)
            return render(request, 'Irapp/search_results.html', {'results': results, 'query': query})
    
    return render(request, 'Irapp/search.html')

def view_document(request, doc_id):
    # Ensure the doc_id corresponds to a document in the document_filenames dictionary
    try:
        doc_id = int(doc_id)
    except ValueError:
        return HttpResponse("Invalid document ID.", status=400)

    doc_filename = document_filenames.get(doc_id)
    if not doc_filename:
        return HttpResponse("Document not found.", status=404)

    try:
        with open(doc_filename, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return HttpResponse("Document not found.", status=404)

    return render(request, 'Irapp/view_document.html', {'content': content, 'doc_filename': os.path.basename(doc_filename)})

