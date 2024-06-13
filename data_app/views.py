from django.shortcuts import render
from data_app.forms import UploadFileForm
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns
# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_csv(file)
            # Perform analysis
            context = {
                'form': form,
                'data': df.head().to_html(),
                'summary': df.describe().to_html(),
                'missing_values': df.isnull().sum().reset_index().rename(columns={0: 'Missing Values'}).to_html(),
                'plots': []
            }

            # Generate plots
            for column in df.select_dtypes(include=['float64', 'int64']).columns:
                fig, ax = plt.subplots()
                sns.histplot(df[column], ax=ax)
                ax.set_title(f'Histogram of {column}')
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close(fig)
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                image_base64 = base64.b64encode(image_png).decode('utf-8')
                context['plots'].append(image_base64)

            return render(request, 'data_app/results.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'data_app/upload.html', {'form': form})
