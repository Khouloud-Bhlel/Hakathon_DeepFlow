import streamlit as st
from PIL import Image
from tesseract import extract
from date_verification import verify_date
from code_verification import verify_code
from cachet_verification import verify_cachet

# Interface Streamlit
st.title("Détection de fraudes documentaires sur les documents de la CNAM")

# Créer un espace pour contrôler l'état d'affichage
if 'run_clicked' not in st.session_state:
    st.session_state['run_clicked'] = False

# Fonction pour réinitialiser l'état du bouton "Run" quand une nouvelle image est téléversée
def reset_state():
    st.session_state['run_clicked'] = False

# Chargement de l'image
uploaded_file = st.file_uploader("Choisissez une image", type=["png", "jpg", "jpeg"], on_change=reset_state)

if uploaded_file is not None:
    # Afficher le bouton "Run" si le bouton n'a pas encore été cliqué
    if not st.session_state['run_clicked']:
        if st.button("Run"):
            # Enregistrer l'état du clic pour cacher l'image téléversée
            st.session_state['run_clicked'] = True

            # Sauvegarder temporairement l'image téléversée
            img = Image.open(uploaded_file)
            image_path = "temp_image.png"
            img.save(image_path)

            # Extraction du texte de l'image
            extracted_text = extract(image_path)

            # Vérification des dates
            verify_date(extracted_text, image_path)
            verify_code(extracted_text, 'output_with_invalid_dates.png')
            verify_cachet('output_with_invalid_dates.png')

            # Affichage du résultat avec les dates invalides
            output_image = Image.open('output_with_invalid_dates.png')
            st.image(output_image, caption="Image avec dates invalides", use_column_width=True)

    else:
        # Si le bouton a été cliqué, afficher directement l'image avec les dates invalides
        output_image = Image.open('output_with_invalid_dates.png')
        st.image(output_image, caption="Image avec dates invalides", use_column_width=True)

    # Afficher l'image téléversée seulement si le bouton "Run" n'a pas été cliqué
    if not st.session_state['run_clicked']:
        img = Image.open(uploaded_file)
        st.image(img, caption="Image téléversée", use_column_width=True)
