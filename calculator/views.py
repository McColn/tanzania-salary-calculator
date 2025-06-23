from django.shortcuts import render

def salary_calculator(request):
    result = None
    if request.method == 'POST':
        try:
            salary_type = request.POST.get('salary_type')  # gross or net
            salary = float(request.POST.get('salary_amount'))

            apply_paye = 'apply_paye' in request.POST
            apply_nssf = 'apply_nssf' in request.POST
            apply_heslb = 'apply_heslb' in request.POST
            apply_nhif = 'apply_nhif' in request.POST

            def calculate_deductions(gross):
                nssf = gross * 0.10 if apply_nssf else 0
                heslb = gross * 0.15 if apply_heslb else 0
                nhif = gross * 0.03 if apply_nhif else 0
                taxable = gross - (nssf + heslb + nhif)
                if apply_paye:
                    if taxable <= 270000:
                        paye = 0
                    elif taxable <= 520000:
                        paye = 0.08 * (taxable - 270000)
                    elif taxable <= 760000:
                        paye = 20000 + 0.20 * (taxable - 520000)
                    elif taxable <= 1000000:
                        paye = 68000 + 0.25 * (taxable - 760000)
                    else:
                        paye = 128000 + 0.30 * (taxable - 1000000)
                else:
                    paye = 0
                total = nssf + heslb + nhif + paye
                take_home = gross - total
                return gross, nssf, heslb, nhif, paye, take_home

            if salary_type == 'gross':
                gross, nssf, heslb, nhif, paye, take_home = calculate_deductions(salary)

            else:  # reverse-calculate gross from net (iteratively)
                # start guessing gross
                estimated_gross = salary
                for _ in range(50):  # converge to correct gross
                    gross, nssf, heslb, nhif, paye, take_home = calculate_deductions(estimated_gross)
                    diff = salary - take_home
                    if abs(diff) < 1:
                        break
                    estimated_gross += diff  # adjust guess

            result = {
                'gross': gross,
                'nssf': nssf if apply_nssf else None,
                'heslb': heslb if apply_heslb else None,
                'nhif': nhif if apply_nhif else None,
                'paye': paye if apply_paye else None,
                'take_home': take_home,
            }
        except Exception as e:
            result = {'error': f'Invalid input: {e}'}

    return render(request, 'calculator/index.html', {'result': result})

