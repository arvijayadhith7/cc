from django.shortcuts import render
from django.http import HttpResponse
from django.apps import apps

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def offerings(request):
    return render(request, "offerings.html")

def category(request):
    model = apps.get_model('law', 'lawtablelist')
    data = model.objects.values('category', 'description').distinct()
    return render(request, "categories.html", {'data': data})

def acts(request, tname):
    model = apps.get_model('law','lawtablelist')
    data = model.objects.filter(category=tname)
    return render(request,"acts.html",{'data':data,'tname':tname})

def chapter(request, tname, act):
    model = apps.get_model('law',act)
    data = model.objects.values('chapter','name').distinct()
    mod = apps.get_model('law','lawtablelist')
    Aname = mod.objects.filter(tname=act)
    return render(request,"chapter.html",{'data':data,'Aname':Aname,'tname':tname,'act':act})

def section(request, tname, act, no):
    model = apps.get_model('law',act)
    data = model.objects.filter(chapter=no) 
    mod = apps.get_model('law','lawtablelist')
    Aname = mod.objects.filter(tname=act)
    return render(request, "section.html", {'data': data,'Aname':Aname, 'tname':tname,'act':act,'cno': no})

def law_detail(request, tname, act, cno, lno):
    model = apps.get_model('law', act)
    data = model.objects.filter(section=lno)
    
    # Get previous and next sections for navigation
    prev_section = model.objects.filter(section=lno-1).first() if lno > 1 else None
    
    # For next section, we need to know if it exists. 
    # Attempt to find the immediate next section. 
    # Note: This assumes sequential sections. If gaps exist, a query like .filter(section__gt=lno).order_by('section').first() is safer but for now we follow the implied logic.
    next_section = model.objects.filter(section=lno+1).first()

    return render(request, "lawdetails.html", {
        'data': data, 
        'tname': tname, 
        'act': act, 
        'chapter_number': cno,
        'prev_section': prev_section,
        'next_section': next_section
    })


# Chatbot View
from django.http import JsonResponse
from django.db.models import Q

def chatbot_response(request):
    if request.method == 'GET':
        query = request.GET.get('message', '').strip()
        if not query:
            return JsonResponse({'response': "Please ask a question."})
        
        results = []
        
        # Models to search in 'law' app
        law_models = [
            'Bns', 'ChildMarriage', 'Electricity', 'IT', 'JuvenileJustice', 
            'MoneyLaundering', 'MotorVehicles', 'NationalHighways', 
            'WomenProtection', 'Wildlife', 'Realestate', 'Water', 
            'Forest', 'Evs', 'Air', 'Companies', 'ConsumerProtection', 'Divorce',
            'ChildProtection', 'PetroleumAndNaturalGas', 'Hindumarriage', 'Specialmarriage'
        ]

        # Models to search in 'right' app
        right_models = [
            'Education', 'ChildLabour', 'HumanRights', 'FoodSecurity', 
            'Information', 'Disabilities', 'SCST', 'LegalServices', 
            'Surrogacy', 'Welfare'
        ]

        # Combine into a list of (app_label, model_name)
        search_targets = [('law', m) for m in law_models] + [('right', m) for m in right_models]
        
        # Pre-fetch law category mapping to avoid N+1 queries
        try:
            law_list_model = apps.get_model('law', 'Lawtablelist')
            law_mapping = {obj.tname: obj.category for obj in law_list_model.objects.all()}
        except:
            law_mapping = {}

        # Search logic
        found = False
        response_text = ""
        
        for app_label, model_name in search_targets:
            try:
                model = apps.get_model(app_label, model_name)
                # Search in title, description, and summary
                matches = model.objects.filter(
                    Q(title__icontains=query) | 
                    Q(description__icontains=query) |
                    Q(summary__icontains=query)
                )[:1] 
                
                for match in matches:
                    found = True
                    
                    title = getattr(match, 'title', 'No Title')
                    section = getattr(match, 'section', '1')
                    chapter = getattr(match, 'chapter', '1')
                    summary = getattr(match, 'summary', '')
                    description = getattr(match, 'description', '')
                    
                    content = summary if summary else (description[:200] + "..." if description else "")
                    context_label = "Legal Framework" if app_label == 'law' else "Human Rights & Welfare"
                    
                    # Construct Detail URL
                    detail_url = "#"
                    if app_label == 'law':
                        category_slug = law_mapping.get(model_name, "Criminal") # Default to Criminal if mapping fails
                        detail_url = f"/categories/{category_slug}/act/{model_name}/chapter_list/chapter/{chapter}/law/{section}/"
                    else:
                        detail_url = f"/right/{model_name}/section/{section}/"

                    response_text += f"""
                    <div style="background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 16px; margin-bottom: 12px; border-left: 4px solid #8B1538; text-align: left;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #eee; padding-bottom: 6px;">
                            <span><strong>{context_label}</strong></span>
                            <span style="color: #8B1538;">{model_name} Hub</span>
                        </div>
                        <h3 style="margin: 0 0 10px 0; color: #1a1a1a; font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 600;">{title}</h3>
                        <div style="margin-bottom: 12px; font-size: 0.85rem; color: #555; display: flex; gap: 8px; flex-wrap: wrap;">
                            <span style="background: #f8f8f8; padding: 4px 8px; border-radius: 4px; border: 1px solid #eee;"><strong>Chapter:</strong> {chapter}</span>
                            <span style="background: #f8f8f8; padding: 4px 8px; border-radius: 4px; border: 1px solid #eee;"><strong>Section:</strong> {section}</span>
                        </div>
                        <div style="font-size: 0.95rem; line-height: 1.6; color: #333; margin-bottom: 12px;">
                            {content}
                        </div>
                        <a href="{detail_url}" target="_blank" style="display: inline-block; background: #8B1538; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 0.85rem; font-weight: 500; transition: background 0.3s;" onmouseover="this.style.background='#6D1029'" onmouseout="this.style.background='#8B1538'">
                            Read Full Section <i class="fas fa-external-link-alt" style="margin-left: 4px; font-size: 0.75rem;"></i>
                        </a>
                    </div>
                    """
                    
                if len(response_text) > 1000: # Limit total response size
                    break
                    
            except LookupError:
                continue
        
        if not found:
            response_text = "I couldn't find specific legal sections matching your query in the database. Please try using keywords like 'murder', 'theft', 'pollution', etc."
        
        return JsonResponse({'response': response_text})

    return JsonResponse({'response': "Invalid request method."})
