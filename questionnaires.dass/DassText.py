from types import MappingProxyType

class DictWrapper:
    def __init__(self, data: dict, databaseName: str):
        self._data = MappingProxyType(data)
        self._databaseName = databaseName

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"Text dictionary [ {self._databaseName} ] has no entry [ {name!r} ]")

def CreateTextEnglish(tc):
   	return {
		"QUESTION": "How much do the statement apply to you over the past week?",
		"I01": "I found myself getting upset by quite trivial things",
		"I02": "I was aware of dryness of my mouth",
		"I03": "I couldn't seem to experience any positive feeling at all",
		"I04": "I experienced breathing difficulty (eg, excessively rapid breathing, breathlessness in the absence of physical exertion)",
		"I05": "I just couldn't seem to get going",
		"I06": "I tended to over-react to situations",
		"I07": "I had a feeling of shakiness (eg, legs going to give way)",
		"I08": "I found it difficult to relax",
		"I09": "I found myself in situations that made me so anxious I was most relieved when they ended",
		"I10": "I felt that I had nothing to look forward to",
		"I11": "I found myself getting upset rather easily ",
		"I12": "I felt that I was using a lot of nervous energy",
		"I13": "I felt sad and depressed",
		"I14": "I found myself getting impatient when I was delayed in any way (for example, elevators, traffic lights, being kept waiting)",
		"I15": "I had a feeling of faintness",
		"I16": "I felt that I had lost interest in just about everything",
		"I17": "I felt I wasn't worth much as a person",
		"I18": "I felt that I was rather touchy",
		"I19": "I perspired noticeably (eg, hands sweaty) in the absence of high temperatures or physical exertion",
		"I20": "I felt scared without any good reason",
		"I21": "I felt that life wasn't worthwhile",
		"I22": "I found it hard to wind down ",
		"I23": "I had difficulty in swallowing",
		"I24": "I couldn't seem to get any enjoyment out of the things I did",
		"I25": "I was aware of the action of my heart in the absence of physical exertion (eg, sense of heart rate increase, heart missing a beat)",
		"I26": "I felt down-hearted and blue",
		"I27": "I found that I was very irritable",
		"I28": "I felt I was close to panic",
		"I29": "I found it hard to calm down after something upset me",
		"I30": "I feared that I would be \"thrown\" by some trivial but unfamiliar task",
		"I31": "I was unable to become enthusiastic about anything",
		"I32": "I found it difficult to tolerate interruptions to what I was doing",
		"I33": "I was in a state of nervous tension",
		"I34": "I felt I was pretty worthless",
		"I35": "I was intolerant of anything that kept me from getting on with what I was doing",
		"I36": "I felt terrified",
		"I37": "I could see nothing in the future to be hopeful about",
		"I38": "I felt that life was meaningless",
		"I39": "I found myself getting agitated",
		"I40": "I was worried about situations in which I might panic and make a fool of myself",
		"I41": "I experienced trembling (eg, in the hands)",
		"I42": "I found it difficult to work up the initiative to do things",
		"L0": "Did not apply to me at all",
		"L1": "Applied to me to some degree, or some of the time",
		"L2": "Applied to me to a considerable degree, or a good part of time",
		"L3": "Applied to me very much, or most of the time"
	}

def CreateTextDanish(tc):
   	return {
		"QUESTION": "Hvor godt du føler udsagnet har passet på dig i den seneste uge?",
		"I01": "Jeg blev bragt ud af ligevægt af ret ligegyldige ting",
		"I02": "Jeg var opmærksom på tørhed i munden",
		"I03": "Jeg kunne ikke opleve nogen som helst positive følelser",
		"I04": "Jeg oplevede vejrtrækningsbesvær (fx udtalt hurtig vejrtrækning, åndenød uden fysisk anstrengelse)",
		"I05": "Jeg kunne bare ikke komme i gang",
		"I06": "Jeg var tilbøjelig til at overreagere på situationer",
		"I07": "Jeg havde en fornemmelse af rysten eller sitren (fx som om benene ville give efter under mig) ",
		"I08": "Jeg havde svært ved at slappe af",
		"I09": "Jeg befandt mig i situationer, der gjorde mig så angst, at jeg var særdeles lettet, når de var overstået",
		"I10": "Jeg følte, at jeg ikke havde noget at se frem til",
		"I11": "Jeg blev meget let blev bragt ud af fatning",
		"I12": "Jeg følte, at jeg brugte en masse psykisk energi",
		"I13": "Jeg følte mig trist og deprimeret",
		"I14": "Jeg blev utålmodig, hvis jeg på nogen måde blev forsinket (fx ved elevatorer, trafiklys, at skulle vente)",
		"I15": "Jeg følte mig svimmel",
		"I16": "Jeg følte, at jeg havde mistet interessen for stort set al",
		"I17": "Jeg følte mig ikke meget værd som person",
		"I18": "Jeg følte mig noget nærtagende",
		"I19": "Jeg svedte mærkbart (fx svedige hænder), selvom det ikke var varmt, og jeg ikke havde anstrengt mig fysisk",
		"I20": "Jeg følte mig bange uden nogen rimelig grund",
		"I21": "Jeg følte, at livet ikke var værd at leve",
		"I22": "Det var svært for mig at slappe af",
		"I23": "Jeg oplevede synkebesvær",
		"I24": "Jeg kunne ikke finde glæde ved de ting, jeg foretog mig",
		"I25": "Jeg var opmærksom på min hjerterytme, selvom jeg ikke anstrengte mig fysisk (fx fornemmelse af øget puls, overspring af hjerteslag)",
		"I26": "Jeg følte mig modløs og trist",
		"I27": "Jeg var meget irritabel",
		"I28": "Jeg følte mig tæt på panik",
		"I29": "Jeg havde svært ved at berolige mig selv, hvis noget bragte mig ud af balance",
		"I30": "Jeg frygtede, at jeg ville blive ”væltet” af en eller anden simpel, men uvant opgave",
		"I31": "Jeg kunne ikke være entusiastisk over noget som helst",
		"I32": "Det var svært at tåle afbrydelser i det, jeg foretog mig",
		"I33": "Jeg var nervøs og anspændt",
		"I34": "Jeg følte mig temmelig værdiløs",
		"I35": "Jeg kunne ikke holde ud at blive afbrudt, når jeg var i gang med noget",
		"I36": "Jeg følte mig rædselsslagen",
		"I37": "Jeg kunne ikke se noget håb for fremtiden",
		"I38": "Jeg følte, at livet var meningsløst",
		"I39": "Jeg følte mig urolig og rastløs ",
		"I40": "Jeg var bekymret for situationer, hvor jeg kunne gå i panik og gøre mig selv til grin",
		"I41": "Jeg oplevede at ryste (fx på hænderne)",
		"I42": "Jeg fandt det svært at tage initiativ til at foretage mig noget",
		"L0": "Passede ikke på mig",
		"L1": "Passede en smule eller noget af tiden på mig",
		"L2": "Passede I betydelig grad eller en stor del af tiden på mig",
		"L3": "Passede rigtigt meget eller det meste af tiden på mig"
	}

def CreateText(tc):
    if tc.Language.casefold() == "da":
          return DictWrapper(CreateTextDanish(tc), "DassText")
    
    return DictWrapper(CreateTextEnglish(tc), "DassText")