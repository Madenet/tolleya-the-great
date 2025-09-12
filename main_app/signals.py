from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import School

@login_required
def school_dashboard_redirect(request):
    # Fetch school names associated with the logged-in user
    user_schools = School.objects.filter(user=request.user).values_list('name', 'id')

    if user_schools.exists():
        if user_schools.count() == 1:
            # Redirect to the only school dashboard
            return redirect('school_dashboard', school_id=user_schools[0][1])  # Access ID from tuple
        else:
            # Pass only names and IDs to the template
            return render(request, 'select_school.html', {'schools': user_schools})
    else:
        # Redirect to a general page or display a message if no school is linked
        return render(request, 'no_school.html')
