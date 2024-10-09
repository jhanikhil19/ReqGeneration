from gptConnection import model
import pandas as pd
from io import StringIO
from fpdf import FPDF

def save_to_pdf(response_text, filename="requirements.pdf"):
    # Create a DataFrame from the CSV data
    df = pd.read_csv(StringIO(response_text), sep="|")

    # Initialize PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add a Unicode font (DejaVuSans.ttf or any other Unicode-supported font)
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)

    # Add title
    pdf.cell(200, 10, text="Requirements Table from Specifications", new_x="LMARGIN", new_y="NEXT", align='C')

    # Calculate column widths based on ratio 10:80:10
    total_width = pdf.w - 5  # Account for page margins
    col_widths = [total_width * 0.20, total_width * 0.70, total_width * 0.10]

    # Add column headers
    headers = df.columns.tolist()
    for i, col in enumerate(headers):
        pdf.cell(col_widths[i], 10, col, border=1, align='C')

    pdf.ln(10)

    # Add table rows with text wrapping in the second column
    for i in range(len(df)):
        for j, col in enumerate(df.columns):
            if j == 1:  # Apply wrapping only for the second column
                pdf.multi_cell(col_widths[j], 10, str(df.iloc[i][col]), border=1)
            else:
                pdf.cell(col_widths[j], 10, str(df.iloc[i][col]), border=1)
            # Move to the next row after multi_cell for column 2
            if j == 1:
                pdf.ln(0)
        pdf.ln(10)  # Move to the next row after each row

    # Save PDF
    pdf.output(filename)

context = f'''
            You are a superb requirement engineer as well as systems engineer who knows everything about Lastenheft, Pflichtenheft. 
            You are responsible for generating Requirements based on ISO standards. 
            You have to adhere all the standards which will be mentioned in the prompt. 
            Also consider the kind of industry and all important compliance for them. 
            Req-ID is AI Generated requirement ID.
            Trace-ID is the ID from the article itself.



            Write professional level of requirements. 
            Give requirement ID as well. 
            You can give output in CSV Format : 
            ***
            Req-ID| Requirement | Trace-ID
            0000001 | The requirments in professional way | 3.2.1 
            ***

            Use | as delimiter for the CSV. 
            Don't put any other header footer apart from the CSV header. 
        '''

prompt = f'''
            ARTICLE 3: AERODYNAMIC COMPONENTS
3.1 Definitions
3.1.1 Aerodynamic Components or Bodywork
All parts of the car in contact with the external air stream.
a. The following components are considered to be bodywork:
i. all components described in Article 3;
ii. inlet or outlet ducts for the purpose of cooling, up to the component they are
intended to provide cooling for;
iii. inlet ducts for the power unit (air boxes) up to the air filter;
iv. primary heat exchangers, as defined in Article 7.4.1 (b).
b. The following components are not considered to be bodywork:
i. cameras and camera housings, as defined in Article 8.17;
ii. rear view mirrors as defined in Article 14.2;
iii. the ERS status light;
iv. parts definitely associated with the mechanical functioning of the power train,
transmission of power to the wheels, and the steering system providing, in any
case, none are of a design contrived to achieve an aerodynamic effect;
v. the wheel rims and tyres;
vi. the brake disc assemblies, calipers and pads.
3.1.2 Frame of Reference
The geometry, component or group of components with respect to which certain bodywork
must remain immobile.
3.1.3 External air stream
The flow of air around the car which has a primary impact on its aerodynamic performance.
3.1.4 Concave and convex curvature
References made in this Article on curvature of aerodynamic surfaces refer to the part of the
aerodynamic surface which is in contact with the external air stream.
When references are made to the curvature of a surface, without specifying an intersection
with a particular plane, the local curvature at any point will be defined as the curvature of the
intersection of the surface in question with a plane passing through a line normal to the
surface at that point. The concave radius of curvature of the surface at that point will be
defined as the minimum concave radius of curvature obtained when the intersecting plane is
swept through 180 degrees around the normal line. The convex radius of curvature of that
surface at that point will be defined as the minimum convex radius of curvature obtained
when the intersecting plane is swept through 180 degrees around the normal line.
As an example, and for the sake of clarity, the aerodynamic surface of a solid sphere would
be the surface where this sphere makes contact with the external airstream, and would be
considered to be a convex surface.
3.1.5 Normal to an aerodynamic surface or curve
The normal applied to an aerodynamic surface at a given point is a vector which is
perpendicular to the surface at that point and points towards the local external air stream.
The normal to a curve at a given point will be considered to be the normal to the surface
containing the curve at the same point.


3.1.6 Tangency Continuity
Tangency Continuity at a given point of a curve or at a given point of a surface, is satisfied if
the value of the tangent is continuous.
Tangency Continuity at intersections between two curves or two surfaces, is satisfied if the
two curves or two surfaces at the intersection are tangent to one another and also have their
normal coincident with each other.
Where two adjacent surfaces are not tangent continuous but could be made so by applying
an edge radius of no more than 1mm along their boundary, these surfaces will be considered
tangent continuous at this boundary whether or not the edge radius is applied, as long as
such an edge radius is permitted according to the relevant article.
3.1.7 Curvature Continuity
Curvature Continuity between two curves, at a given point of a curve, between two surfaces
or within a surface is satisfied if the value of the curvature is continuous and in the same
direction.
3.1.8 Open and closed sections
Within the prescribed limitations of the relevant regulation, a section through the bodywork
when intersected with a defined plane will be considered closed if it forms a complete
boundary by itself otherwise it will be considered open.
3.1.9 Fillet and Edge Radius
A fillet radius is formed by rounding an internal corner (included angle less than 180 degrees)
with a concave surface, whilst an edge radius is created by smoothing an external corner
(included angle greater than 180 degrees) through material removal, resulting in a convex
surface.
In both cases the resultant surface must be formed by arcs with radius of curvature
respecting the limit(s) specified, connecting two fully defined surfaces tangentially with no
inflection and perpendicular to the intersection between them. Unless otherwise specified,
both fillet and edge radii may change in magnitude around the periphery of the boundary
around which they are defined, but such changes must be continuous.
If there exists a discontinuity in tangency at the trailing edge of the intersection between the
parts to be joined by a fillet radius, then a closed aerodynamic fairing may be added
immediately behind the trailing edge. This fairing must be no larger in cross section than the
preceding fillet radius and any trailing edge immediately adjacent to the fillet and no longer
than three times the maximum fillet arc radius at this point.
3.1.10 Aerodynamic seal
The function by which the flow between two regions of different pressure is kept to the
minimum feasible magnitude.
3.1.11 Gurney
A component fitted to the trailing edge of a profile in order to adjust its aerodynamic
performance. In any plane normal to the trailing edge of the profile, the Gurney must contain
a flat section no more than 1mm thick, and of a given height (defined as the size of the
Gurney), and a bonding flange onto the surface of the wing which may be no more than
20mm long and 1mm thick. No part of the Gurney may protrude behind a line that is normal
to the surface on which the Gurney is applied at the point of the trailing edge of the profile.


3.2 General Principles and Legality Checking
3.2.1 Objective of Article 3
An important objective of the Regulations in Article 3 is to enable cars to race closely, by
ensuring that the aerodynamic performance loss of a car following another car is kept to a
minimum. In order to verify whether this objective has been achieved, Competitors may be
required on request to supply the FIA with any relevant information.


n any case the Intellectual Property of this information, will remain the property of the
Competitor, will be protected and not divulged to any third party.
3.2.2 Aerodynamic Influence
With the exception of the driver adjustable bodywork described in Article 3.10.10 (in addition
to minimal parts solely associated with its actuation) and the flexible seals specifically
permitted by Articles 3.13 and 3.14.4, all aerodynamic components or bodywork influencing
the car’s aerodynamic performance must be rigidly secured and immobile with respect to
their frame of reference defined in Article 3.3. Furthermore, these components must produce
a uniform, solid, hard, continuous, impervious surface under all circumstances.
Any device or construction that is designed to bridge the gap between the sprung part of the
car and the ground is prohibited under all circumstances.
With the exception of the parts necessary for the adjustment described in Article 3.10.10, or
any incidental movement due to the steering system, any car system, device or procedure
which uses driver movement as a means of altering the aerodynamic characteristics of the
car is prohibited.
The Aerodynamic influence of any component of the car not considered to be bodywork must
be incidental to its main function. Any design which aims to maximise such an aerodynamic
influence is prohibited.
3.2.3 Symmetry
All bodywork must be nominally symmetrical with respect to Y=0. Consequently, and unless
otherwise specified, any regulation in Article 3 concerning one side of the car will be assumed
to be valid for the other side of the car and references to maximum permissible numbers of
components in Article 3 will also refer to the one side of the car.
Minimal exceptions to the requirement of symmetry of this Article will be accepted for the
installation of non-symmetrical mechanical components of the car, for asymmetrical cooling
requirements or for asymmetrical angle adjustment of the front flap defined in Article 3.9.7.
Bodywork on the unsprung mass must respect this Article when the suspension position of
each wheel is virtually re-orientated so that its wheel coordinate system axes (described in
Article 2.11.3) are parallel to their respective axis of the car coordinate system (described in
Article 2.11.1).
3.2.4 Digital legality checking
The assessment of the car’s compliance with the Aerodynamic Regulations will be carried out
digitally using CAD models provided by the teams. In these models:
a. Components may only be designed to the edge of a Reference Volume or with a precise
geometrical feature, or to the limit of a geometrical criterion (save for the normal
round-off discrepancies of the CAD system), when the regulations specifically require an
aspect of the bodywork to be designed to this limit, or it can be demonstrated that the
design does not rely on lying exactly on this limit to conform to the regulations, such
that it is possible for the physical bodywork to comply.
b. Components which must follow a precise shape, surface or plane must be designed
without any tolerance, save for the normal round-off discrepancies of the CAD system.
3.2.5 Physical legality checking
The cars may be measured during a Competition in order to check their conformance to the
CAD models discussed in Article 3.2.4 and to ensure they remain inside the Reference
Volumes.
a. Unless otherwise specified, a tolerance of ±3mm will be accepted for manufacturing
purposes only with respect to the CAD surfaces. Where measured surfaces lie outside of
this tolerance but remain within the Reference Volumes, a Competitor may be required
to provide additional information (e.g. revised CAD geometry) to demonstrate
compliance with the regulations. Any discrepancies contrived to create a special
aerodynamic effect or surface finish will not be permitted.

b. Irrespective of a), geometrical discrepancies at the limits of the Reference Volumes
must be such that the measured component remains inside the Reference Volume.
c. A positional tolerance of +/- 2mm will be accepted for the Front Wing Bodywork, Rear
Wing Bodywork, Exhaust Tailpipe, Floor Bodywork behind X R =0, and Tail. This will be
assessed by realigning each of the groups of Reference Volumes and Reference Surfaces
that define the assemblies, by up to 2mm from their original position, to best fit the
measured geometry.
d. Irrespective of b), a tolerance of Z=+/-2mm will be accepted for parts of the car lying on
the Z=0 plane, with -375 ≤ Y ≤ 375 and ahead of X R=0.
e. Minimal discrepancies from the CAD surfaces will also be accepted in the following
cases:
i. Minimal repairs carried out on aerodynamic components and approved by the FIA
ii. Tape, provided it does not achieve an aerodynamic effect otherwise not
permitted by Article 3
iii. Junctions between bodywork panels
iv. Local bodywork fixing details
3.2.6 Datum Points
All cars must be equipped with mountings for optical targets that enable the car’s datum to
be determined for scrutineering in the following locations:
i. One on the forward part of the top of the survival cell.
ii. Two positioned symmetrically about Y=0 on the top of the survival cell close to XB =0.
iii. Two positioned symmetrically about Y=0 on the side of the survival cell close to X B =0.
iv. Two positioned symmetrically about Y=0 on the side of the survival cell close to the rear
mounts of the secondary roll structure.
v. Two positioned symmetrically about Y=0 within an axis-aligned cuboid with an interior
diagonal defined by points [X C =0, 175, 970] and [X C =150, -175, 870].
vi. One probed point on the RIS or gearbox case.
In all cases, a file with required datum points must be supplied for each survival cell.
For deflection testing, all cars must be provided with a means of mounting a reference
artefact to the RIS. This mounting may be temporary, but must be rigid with respect to the
underlying car structure.
Full details of the requirements are given in the Appendix the Technical and Sporting
Regulations.
3.2.7 Section titles and Article titles within this article have no regulatory value.
3.2.8 Static pressure tappings are permitted in surfaces, provided that they;
i. Have an internal diameter of no more than 2mm.
ii. They are flush with the underlying geometry.
iii. Are only connected to pressure sensors, or are blanked, without leakage.

        '''


response = model.generate_content(context+prompt)
# print("RESPONSE:",response.text)
print("Usage Metadata:",response.usage_metadata)
print("Prompt Feedback",response.prompt_feedback)

save_to_pdf(response.text, "requirements.pdf")

# print("Citations: ", response)