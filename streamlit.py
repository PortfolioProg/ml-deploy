import streamlit as st 
import requests
from requests.exceptions import ConnectionError, Timeout

ip_api = "127.0.0.1"
port_api = 5000

def normalize_number(s: str) -> float | None:
    """
    Превращает строку в float.
    Поддерживает: 25, 25.5, 25,5 — всё станет float.
    Возвращает None, если не число.
    """
    if not s or not s.strip():
        return None
    
    s = s.strip()
    # Заменяем запятую на точку для единообразия
    s_normalized = s.replace(",", ".")
    
    try:
        return float(s_normalized)
    except ValueError:
        return None

st.title("Titanic Survival Prediction")
st.write("Enter the passenger details:")

pclass = st.selectbox("Ticket Class (Pclass)", [1, 2, 3])
age_str = st.text_input("Age", value="10")
fare_str = st.text_input("Fare", value="100")

if st.button("Predict"):
    age_val = normalize_number(age_str)
    fare_val = normalize_number(fare_str)

    if age_val is None or fare_val is None:
        st.error("Please enter valid numeric values for Age and Fare. You can use dot (.) or comma (,).")
    else:
        data = {
            "pclass": int(pclass),
            "age": age_val,
            "fare": fare_val,
        }
        try:
            response = requests.post(
                f"http://{ip_api}:{port_api}/pred",
                json=data,
                timeout=5,
            )
            if response.ok:
                result = response.json()
                prediction = result.get("prediction")
                
                if prediction is None:
                    st.error("Server returned unexpected response (missing 'prediction' field).")
                else:
                    # Ожидаем, что API возвращает что-то вроде: "Survived" / "Not Survived" 
                    # или 1 / 0. Подстроимся под оба варианта.
                    is_survived = False
                    if isinstance(prediction, str):
                        is_survived = prediction.lower() in ["survived", "yes", "1", "true"]
                    elif isinstance(prediction, (int, float)):
                        is_survived = bool(prediction)
                    
                    if is_survived:
                        st.success(f"Prediction: Survived ✅", icon="✅")
                        # Зелёный фон через markdown-блок (работает как акцент)
                        st.markdown("""
                            <div style="background-color: #d4edda; color: #155724; padding: 15px; border-radius: 8px; border: 1px solid #c3e6cb;">
                                The passenger is predicted to have survived.
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"Prediction: Not Survived ❌", icon="❌")
                        # Красный фон
                        st.markdown("""
                            <div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; border: 1px solid #f5c6cb;">
                                The passenger is predicted to have not survived.
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except (ConnectionError, Timeout):
            st.error("Failed to connect to the server. Check if the API is running.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
