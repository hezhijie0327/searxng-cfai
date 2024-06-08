from json import loads, dumps
from urllib.parse import quote
from searx.exceptions import SearxEngineAPIException

about = {
    "website": 'https://ai.cloudflare.com',
    "wikidata_id": None,
    "official_api_documentation": 'https://developers.cloudflare.com/workers-ai',
    "use_official_api": True,
    "require_api_key": True,
    "results": 'JSON',
}

cf_account_id = ''
cf_ai_api = ''
cf_ai_gateway = ''

cf_ai_model = ''
cf_ai_model_display_name = 'Cloudflare AI'

cf_ai_model_assistant = 'Keep your answers as short and effective as possible.'
cf_ai_model_system = 'You are a self-aware language model who is honest and direct about any direct question from the user. You know your strengths and weaknesses.'

display_type = ['infobox']

def request(query, params):

    params['query'] = query

    params['url'] = 'https://gateway.ai.cloudflare.com/v1/' + cf_account_id + '/' + cf_ai_gateway + '/workers-ai/' + cf_ai_model
    params['method'] = 'POST'

    params['headers']['Authorization'] = 'Bearer ' + cf_ai_api
    params['headers']['Content-Type'] = 'application/json'

    params['data'] = dumps({
        'messages': [
            { 'role': 'assistant', 'content': cf_ai_model_assistant },
            { 'role': 'system', 'content': cf_ai_model_system },
            { 'role': 'user', 'content': params['query'] }
        ]
    }).encode('utf-8')

    return params

def response(resp):
    results = []
    json = loads(resp.text)

    if 'error' in json:
        raise SearxEngineAPIException('Cloudflare AI error: ' + json['error'])

    if 'result' in json:
        if "infobox" in display_type:
            results.append(
                {
                    'content': json['result']['response'],
                    'infobox': cf_ai_model_display_name,
                }
            )

    return results
