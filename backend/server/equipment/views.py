import io
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER

from .models import Dataset, Equipment
from .serializers import (
    DatasetListSerializer,
    DatasetDetailSerializer,
    SummarySerializer,
    EquipmentSerializer,
    UserRegistrationSerializer,
    LoginSerializer,
)


MAX_DATASETS_PER_USER = 5


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login and get auth token."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout and delete auth token."""
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Upload CSV file and create dataset with equipment records."""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_csv(csv_file)
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            return Response(
                {'error': f'Missing columns: {missing_cols}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Enforce 5-dataset limit
        user_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
        if user_datasets.count() >= MAX_DATASETS_PER_USER:
            oldest = user_datasets.last()
            oldest.delete()
        
        # Reset file pointer and save
        csv_file.seek(0)
        dataset = Dataset.objects.create(
            name=csv_file.name,
            user=request.user,
            file=csv_file
        )
        
        # Create equipment records
        equipment_list = []
        for _, row in df.iterrows():
            equipment_list.append(Equipment(
                dataset=dataset,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=float(row['Flowrate']),
                pressure=float(row['Pressure']),
                temperature=float(row['Temperature'])
            ))
        Equipment.objects.bulk_create(equipment_list)
        
        return Response(
            DatasetDetailSerializer(dataset).data, 
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DatasetViewSet(viewsets.ModelViewSet):
    """ViewSet for dataset operations."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DatasetListSerializer
        return DatasetDetailSerializer
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get summary statistics for a dataset."""
        dataset = self.get_object()
        equipment = dataset.equipment.all()
        
        if not equipment.exists():
            return Response({'error': 'No equipment data'}, status=status.HTTP_404_NOT_FOUND)
        
        type_distribution = {}
        for eq in equipment:
            type_distribution[eq.equipment_type] = type_distribution.get(eq.equipment_type, 0) + 1
        
        summary_data = {
            'total_count': equipment.count(),
            'avg_flowrate': sum(e.flowrate for e in equipment) / equipment.count(),
            'avg_pressure': sum(e.pressure for e in equipment) / equipment.count(),
            'avg_temperature': sum(e.temperature for e in equipment) / equipment.count(),
            'type_distribution': type_distribution,
        }
        
        return Response(SummarySerializer(summary_data).data)
    
    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Generate PDF report for a dataset with charts."""
        dataset = self.get_object()
        equipment = list(dataset.equipment.all())
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            textColor=colors.HexColor('#1e293b'),
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#334155')
        )
        
        # Title
        elements.append(Paragraph(f"Equipment Report: {dataset.name}", title_style))
        elements.append(Spacer(1, 10))
        
        # Summary Statistics
        if equipment:
            count = len(equipment)
            avg_flow = sum(e.flowrate for e in equipment) / count
            avg_press = sum(e.pressure for e in equipment) / count
            avg_temp = sum(e.temperature for e in equipment) / count
            
            # Summary cards as a table
            summary_data = [
                ['Total Equipment', 'Avg Flowrate', 'Avg Pressure', 'Avg Temperature'],
                [str(count), f'{avg_flow:.2f}', f'{avg_press:.2f}', f'{avg_temp:.2f}']
            ]
            summary_table = Table(summary_data, colWidths=[1.8*inch]*4)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f1f5f9')),
                ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#1e293b')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, 1), 18),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('LINEBEFORE', (1, 0), (1, -1), 1, colors.HexColor('#cbd5e1')),
                ('LINEBEFORE', (2, 0), (2, -1), 1, colors.HexColor('#cbd5e1')),
                ('LINEBEFORE', (3, 0), (3, -1), 1, colors.HexColor('#cbd5e1')),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 20))
            
            # Generate Type Distribution Chart
            type_distribution = {}
            for eq in equipment:
                type_distribution[eq.equipment_type] = type_distribution.get(eq.equipment_type, 0) + 1
            
            if type_distribution:
                fig1, ax1 = plt.subplots(figsize=(7, 3.5))
                types = list(type_distribution.keys())
                counts = list(type_distribution.values())
                
                # Create gradient-like bar colors
                bar_colors = ['#64748b'] * len(types)
                bars = ax1.bar(types, counts, color=bar_colors, edgecolor='#334155', linewidth=0.5)
                
                ax1.set_ylabel('Count', fontsize=10, color='#334155')
                ax1.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', color='#1e293b', pad=15)
                ax1.set_xticklabels(types, rotation=45, ha='right', fontsize=8)
                ax1.tick_params(axis='y', labelsize=8, colors='#64748b')
                ax1.tick_params(axis='x', colors='#64748b')
                ax1.spines['top'].set_visible(False)
                ax1.spines['right'].set_visible(False)
                ax1.spines['left'].set_color('#cbd5e1')
                ax1.spines['bottom'].set_color('#cbd5e1')
                ax1.set_facecolor('#f8fafc')
                fig1.patch.set_facecolor('#ffffff')
                
                plt.tight_layout()
                
                chart1_buffer = io.BytesIO()
                plt.savefig(chart1_buffer, format='png', dpi=150, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                chart1_buffer.seek(0)
                plt.close(fig1)
                
                chart1_img = Image(chart1_buffer, width=6.5*inch, height=3*inch)
                elements.append(chart1_img)
                elements.append(Spacer(1, 15))
            
            # Generate Parameter Chart (Line chart)
            if len(equipment) > 1:
                fig2, ax2 = plt.subplots(figsize=(7, 3.5))
                
                names = [eq.equipment_name for eq in equipment]
                flowrates = [eq.flowrate for eq in equipment]
                pressures = [eq.pressure for eq in equipment]
                temperatures = [eq.temperature for eq in equipment]
                
                x = np.arange(len(names))
                
                ax2.plot(x, flowrates, marker='s', label='Flowrate', color='#64748b', linewidth=2, markersize=6)
                ax2.plot(x, pressures, marker='s', label='Pressure', color='#94a3b8', linewidth=2, markersize=6)
                ax2.plot(x, temperatures, marker='o', label='Temperature', color='#1e293b', linewidth=2, markersize=6)
                
                ax2.set_ylabel('Value', fontsize=10, color='#334155')
                ax2.set_title('Equipment Parameters', fontsize=14, fontweight='bold', color='#1e293b', pad=15)
                ax2.set_xticks(x)
                ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=7)
                ax2.tick_params(axis='y', labelsize=8, colors='#64748b')
                ax2.tick_params(axis='x', colors='#64748b')
                ax2.legend(loc='upper right', fontsize=8, framealpha=0.9)
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.spines['left'].set_color('#cbd5e1')
                ax2.spines['bottom'].set_color('#cbd5e1')
                ax2.set_facecolor('#f8fafc')
                ax2.grid(True, linestyle='--', alpha=0.3, color='#cbd5e1')
                fig2.patch.set_facecolor('#ffffff')
                
                plt.tight_layout()
                
                chart2_buffer = io.BytesIO()
                plt.savefig(chart2_buffer, format='png', dpi=150, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
                chart2_buffer.seek(0)
                plt.close(fig2)
                
                chart2_img = Image(chart2_buffer, width=6.5*inch, height=3*inch)
                elements.append(chart2_img)
                elements.append(Spacer(1, 20))
        
        # Equipment table
        elements.append(Paragraph("Equipment Data", heading_style))
        table_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for eq in equipment:
            table_data.append([
                eq.equipment_name,
                eq.equipment_type,
                f"{eq.flowrate:.2f}",
                f"{eq.pressure:.2f}",
                f"{eq.temperature:.2f}"
            ])
        
        col_widths = [2*inch, 1.5*inch, 1*inch, 1*inch, 1*inch]
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#334155')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.HexColor('#f1f5f9')]),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1e293b')),
            ('LINEBELOW', (0, 1), (-1, -2), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        elements.append(table)
        
        doc.build(elements)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.name}_report.pdf"'
        return response

