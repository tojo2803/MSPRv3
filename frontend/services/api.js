import axios from 'axios';

// Récupère le pays/langue sélectionné (ex: 'fr', 'us', 'ch_fr', 'ch_en', 'ch_de')
const country = localStorage.getItem("selectedCountry") || "fr";
console.log(localStorage.getItem("selectedCountry"));

let baseURL;
if (country === "fr" || country === "us") {
  baseURL = `/api/${country}/`;
} else if (country.startsWith("ch_")) {
  // country = 'ch_fr', 'ch_en', 'ch_de'
  const lang = country.split("_")[1];
  baseURL = `/api/ch/${lang}/`;
} else {
  baseURL = `/api/fr/`; // fallback
}

const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Récupère les données de mortalité US avec pagination et filtrage par année.
 * @param {number} page - Numéro de page (défaut 1)
 * @param {number} pageSize - Nombre d'éléments par page (défaut 100)
 * @param {number|null} year - Année à filtrer (optionnel)
 * @returns {Promise<Array>} - Tableau de résultats
 */
export async function fetchUSMortalite(page = 1, pageSize = 100, year = null) {
  const offset = (page - 1) * pageSize;
  let url = `mortalite/?offset=${offset}&limit=${pageSize}`;
  if (year) url += `&year=${year}`;
  const response = await apiClient.get(url);
  return response.data;
}

export default apiClient;